import logging

from aiohttp.web import HTTPError, HTTPInternalServerError, Response

from playlog.lib.validation import ValidationError
from playlog.web.framework.status import HTTP_BAD_REQUEST, HTTP_OK, HTTP_INTERNAL_SERVER_ERROR
from playlog.web.framework.response import ErrorResponse, json_response


logger = logging.getLogger(__name__)


async def error_middleware(app, next_handler):
    async def handler(request):
        try:
            result = await next_handler(request)
        except Exception as exc:
            if isinstance(exc, ValidationError):
                result = ErrorResponse(
                    data=exc.errors,
                    status=HTTP_BAD_REQUEST
                )
            elif not isinstance(exc, HTTPError):
                message = 'An error has occurred'
                logger.exception(message)
                result = ErrorResponse(
                    data={'message': message},
                    status=HTTP_INTERNAL_SERVER_ERROR
                )
            else:
                raise exc  # TODO: format response
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
                    status = HTTP_OK
                result = json_response(data, status=status)
            else:
                logger.error('Unable to serialize response (accept=%s)', accept)
                raise HTTPInternalServerError()
        return result
    return handler
