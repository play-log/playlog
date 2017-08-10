import logging

from aiohttp.web import Response


logger = logging.getLogger(__name__)


async def submissions_middleware(app, next_handler):
    """
    Submissions authentication
    See https://www.last.fm/api/submissions
    """
    async def handler(request):
        if request.path in ['/submissions/submit', '/submissions/nowplay']:
            session_id = (await request.post()).get('s')
            if not (await request.app['session'].verify(session_id)):
                logger.warn('Submissions request aborted (bad session: %s)', session_id)
                return Response(text='BADSESSION')
        return await next_handler(request)
    return handler


MIDDLEWARES = [submissions_middleware]
