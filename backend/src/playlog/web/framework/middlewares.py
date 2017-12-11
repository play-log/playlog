import logging

from aiohttp.web import HTTPException, HTTPBadRequest, Response

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
                    data={
                        'message': 'Validation error',
                        'errors': exc.errors
                    },
                    status=HTTP_BAD_REQUEST
                )
            elif not isinstance(exc, HTTPException):
                message = 'An error has occurred'
                logger.exception(message)
                result = ErrorResponse(
                    data={'message': message},
                    status=HTTP_INTERNAL_SERVER_ERROR
                )
            else:
                if exc.empty_body:
                    # currently we dont use exceptions without body
                    # so don't cover this line for a while
                    raise exc  # pragma: no cover
                result = ErrorResponse(
                    data={'message': exc.reason},
                    status=exc.status,
                    headers=exc.headers
                )
        return result
    return handler


async def response_middleware(app, next_handler):
    async def handler(request):
        result = await next_handler(request)
        if not isinstance(result, Response):
            accept = request.headers.get('accept', 'application/json')
            if accept in ('application/json', '*/*'):
                if isinstance(result, ErrorResponse):
                    data, status, headers = result.data, result.status, result.headers
                    if headers:
                        # Passing both Content-Type header
                        # and content_type or charset params is forbidden
                        # (json_response already passes content_type)
                        headers.pop('content-type', None)
                else:
                    data, status, headers = result, HTTP_OK, None
                result = json_response(data, status=status, headers=headers)
            else:
                logger.error('Unable to serialize response (accept=%s)', accept)
                raise HTTPBadRequest()
        return result
    return handler
