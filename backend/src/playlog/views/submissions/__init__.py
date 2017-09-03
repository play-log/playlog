import logging

from hashlib import md5

from aiohttp.web import Response

from playlog import config
from playlog.decorators import route
from playlog.views import View


logger = logging.getLogger(__name__)

PROTOCOL_VERSIONS = ['1.2', '1.2.1']


@route('/submissions/')
class Submissions(View):
    async def get(self):
        logger.info('Handshake started')

        query = self.request.query
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

        expected_token = md5(config.SUBMISSIONS['password_hash'].encode('utf-8'))
        timestamp = query.get('t', '')
        expected_token.update(timestamp.encode('utf-8'))
        token = query.get('a')
        if token != expected_token.hexdigest():
            logger.warn('Handshake failed with invalid token: %s', token)
            return Response(text='BADAUTH')

        session_id = await self.session.create()
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
