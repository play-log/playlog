import logging

from datetime import datetime
from hashlib import md5
from time import time

from aiohttp.web import Response

from playlog import config
from playlog.actions import artist, album, nowplay, play, track
from playlog.web.framework.decorators import autowired, route


logger = logging.getLogger(__name__)

PROTOCOL_VERSIONS = ['1.2', '1.2.1']
NOWPLAY_KEYMAP = [
    ('artist', 'a'),
    ('album', 'b'),
    ('title', 't'),
    ('length', 'l')
]
SUBMISSION_KEYMAP = [
    ('artist', 'a'),
    ('album', 'b'),
    ('track', 't'),
    ('timestamp', 'i')
]
MAX_SUBMISSIONS = 50


@route.get('/submissions/')
@autowired
async def submissions_handshake(request, session):
    logger.info('Handshake started')

    query = request.query
    if query.get('hs') != 'true':
        return Response(text='Audioscrobbler submissions system')

    protocol_version = query.get('p')
    if protocol_version not in PROTOCOL_VERSIONS:
        logger.warn('Handshake failed with invalid protocol version: %s', protocol_version)
        return Response(text='FAILED Incorrect protocol version')

    username = query.get('u')
    if username != config.SUBMISSIONS['username']:
        logger.warn('Handshake failed with invalid username: %s', username)
        return Response(text='BADAUTH')

    timestamp = query.get('t', '')
    try:
        timestamp = int(timestamp)
    except ValueError:
        logger.warn('Handshake failed with invalid timestamp: %s', timestamp)
        return Response(text='FAILED Bad timestamp')

    delay = abs(int(time()) - timestamp)
    if delay > config.SUBMISSIONS['handshake_timeout']:
        msg = 'Handshake timeout exceeded: %d > %d'
        logger.warn(msg, delay, config.SUBMISSIONS['handshake_timeout'])
        return Response(text='FAILED Bad timestamp')

    expected_token = md5(config.SUBMISSIONS['password_hash'].encode('utf-8'))
    expected_token.update(str(timestamp).encode('utf-8'))
    token = query.get('a')
    if token != expected_token.hexdigest():
        logger.warn('Handshake failed with invalid token: %s', token)
        return Response(text='BADAUTH')

    session_id = await session.create()
    logger.info('Handshake succeeded (Session ID: %s)', session_id)

    base_url = '{}/submissions'.format(config.SUBMISSIONS['base_url'])
    nowplay_url = '{}/nowplay'.format(base_url)
    submissions_url = '{}/submit'.format(base_url)

    return Response(text='\n'.join([
        'OK',
        session_id,
        nowplay_url,
        submissions_url
    ]))


@route.post('/submissions/nowplay')
@autowired
async def submissions_nowplay(request, redis):
    post = await request.post()
    data = {a: post.get(b, '').strip() for a, b in NOWPLAY_KEYMAP}
    try:
        data['length'] = int(data['length'])
    except ValueError:
        logger.warn('Invalid length of current track: %s', data)
    else:
        if all(data.values()):
            logger.info('Setting current track: %s', data)
            await nowplay.set_track(redis, **data)
        else:
            logger.warn('Unable to set current track: %s', data)
    return Response(text='OK')


def parse_submissions(data):
    result = []
    for i in range(0, MAX_SUBMISSIONS):
        submission = {a: data.get('{}[{}]'.format(b, i), '').strip() for a, b in SUBMISSION_KEYMAP}
        if not all(submission.values()):
            break
        try:
            submission['timestamp'] = int(submission['timestamp'])
        except ValueError:
            logger.warn('Invalid submission timestamp (%s), skipping', submission)
            continue
        else:
            submission['date'] = datetime.fromtimestamp(submission.pop('timestamp'))
            result.append(submission)
    return result


async def handle_artist(conn, name):
    data = await artist.find_one(conn, name=name)
    if data:
        artist_id = data['id']
        await artist.update(conn, artist_id)
    else:
        artist_id = await artist.create(conn, name)
    return artist_id


async def handle_album(conn, artist_id, name):
    data = await album.find_one(conn, artist_id=artist_id, name=name)
    if data:
        album_id = data['id']
        await album.update(conn, album_id)
    else:
        album_id = await album.create(conn, artist_id, name)
    return album_id


async def handle_track(conn, album_id, name):
    data = await track.find_one(conn, album_id=album_id, name=name)
    if data:
        track_id = data['id']
        await track.update(conn, track_id)
    else:
        track_id = await track.create(conn, album_id, name)
    return track_id


@route.post('/submissions/submit')
@autowired
async def submissions_submit(request, db):
    submissions = parse_submissions(await request.post())
    for item in submissions:
        if await play.is_date_exists(db, item['date']):
            logger.warn(
                'Unable to handle submission: '
                'date already exists (%s)',
                item['date']
            )
            continue
        artist_id = await handle_artist(db, item['artist'])
        album_id = await handle_album(db, artist_id, item['album'])
        track_id = await handle_track(db, album_id, item['track'])
        await play.create(db, track_id, item['date'])
    return Response(text='OK')
