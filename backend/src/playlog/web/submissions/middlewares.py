import logging

from aiohttp.web import Response

from playlog.actions import session


logger = logging.getLogger(__name__)


async def submissions_middleware(app, next_handler):
    """
    Submissions authentication
    See https://www.last.fm/api/submissions
    """
    async def handler(request):
        if request.path in ['/submissions/submit', '/submissions/nowplay']:
            sid = (await request.post()).get('s')
            if not (await session.verify(request.app['redis'], sid)):
                logger.warn('Submissions request aborted (bad session: %s)', sid)
                return Response(text='BADSESSION')
        return await next_handler(request)
    return handler
