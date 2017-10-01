import logging

from aiohttp.web import HTTPInternalServerError, Response, json_response
from playlog.lib.json import dumps as json_encode

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


async def response_middleware(app, next_handler):
    async def handler(request):
        result = await next_handler(request)
        if not isinstance(result, Response):
            accept = request.headers.get('accept')
            if accept == 'application/json':
                result = json_response(result, dumps=json_encode)
            else:
                logger.error('Unable to serialize response (accept=%s)', accept)
                raise HTTPInternalServerError()
        return result
    return handler


MIDDLEWARES = [submissions_middleware, response_middleware]
