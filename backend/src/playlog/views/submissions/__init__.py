import logging

from hashlib import md5
from time import time

from aiohttp.web import Response

from playlog import config
from playlog.decorators import route


logger = logging.getLogger(__name__)

PROTOCOL_VERSIONS = ['1.2', '1.2.1']


@route.get('/submissions/')
async def submissions(request):
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

    session_id = await request.app['session'].create()
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
