import functools

from aiohttp.web import json_response as _json_response

from playlog.lib.json import dumps as json_encode


__all__ = ['ErrorResponse', 'json_response']


class ErrorResponse(object):
    def __init__(self, *, data, status, headers=None):
        self.data = data
        self.status = status
        self.headers = headers


json_response = functools.partial(_json_response, dumps=json_encode)
