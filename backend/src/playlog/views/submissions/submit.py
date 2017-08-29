import logging

from datetime import datetime

from aiohttp.web import Response

from playlog.decorators import route
from playlog.models import artist, album, play, track
from playlog.views import View


logger = logging.getLogger(__name__)

MAX_SUBMISSIONS = 50

KEYMAP = [
    ('artist', 'a'),
    ('album', 'b'),
    ('track', 't'),
    ('timestamp', 'i')
]


def parse_submissions(data):
    result = []
    for i in range(0, MAX_SUBMISSIONS):
        submission = {a: data.get('{}[{}]'.format(b, i), '').strip() for a, b in KEYMAP}
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


@route('/submissions/submit')
class Submit(View):
    async def post(self):
        submissions = parse_submissions(await self.request.post())
        async with self.db as conn:
            for item in submissions:
                if await play.is_date_exists(conn, item['date']):
                    logger.warn(
                        'Unable to handle submission: '
                        'date already exists (%s)',
                        item['date']
                    )
                    continue
                artist_id = await handle_artist(conn, item['artist'])
                album_id = await handle_album(conn, artist_id, item['album'])
                track_id = await handle_track(conn, album_id, item['track'])
                await play.create(conn, track_id, item['date'])
        return Response(text='OK')
