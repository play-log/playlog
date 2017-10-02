import logging

from aiohttp.web import HTTPError, HTTPInternalServerError, Response, json_response
from playlog.lib.json import dumps as json_encode
from playlog.lib.validation import ValidationError

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


class ErrorResponse(object):
    def __init__(self, *, data, status):
        self.data = data
        self.status = status


async def error_middleware(app, next_handler):
    async def handler(request):
        try:
            result = await next_handler(request)
        except Exception as exc:
            if isinstance(exc, ValidationError):
                result = ErrorResponse(data=exc.errors, status=400)
            elif not isinstance(exc, HTTPError):
                message = 'An error has occurred'
                logger.exception(message)
                result = ErrorResponse(data={'message': message}, status=500)
            else:
                raise exc
        return result
    return handler


async def response_middleware(app, next_handler):
    async def handler(request):
        result = await next_handler(request)
        if not isinstance(result, Response):
            accept = request.headers.get('accept')
            if accept == 'application/json':
                if isinstance(result, ErrorResponse):
                    data = result.data
                    status = result.status
                else:
                    data = result
                    status = 200
                result = json_response(data, status=status, dumps=json_encode)
            else:
                logger.error('Unable to serialize response (accept=%s)', accept)
                raise HTTPInternalServerError()
        return result
    return handler


MIDDLEWARES = [submissions_middleware, response_middleware, error_middleware]
