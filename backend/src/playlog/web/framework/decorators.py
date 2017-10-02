import functools
import inspect

import venusian

from aiohttp import hdrs


__all__ = ['autowired', 'route']


def autowired(func):
    keys = [k for k in inspect.signature(func).parameters.keys()][1:]

    @functools.wraps(func)
    async def wrapper(request):
        kwargs = {key: request.app[key] for key in keys}
        if 'db' in kwargs:
            async with request.app['db'].acquire() as conn:
                kwargs['db'] = conn
                result = await func(request, **kwargs)
        else:
            result = await func(request, **kwargs)
        return result
    return wrapper


class route:
    def __init__(self, path, method):
        self.method = method
        self.path = path

    def __call__(self, view):
        def callback(scanner, name, ob):
            scanner.router.add_route(self.method, self.path, view)
        venusian.attach(view, callback)
        return view

    @classmethod
    def get(cls, path):
        return cls(path, hdrs.METH_GET)

    @classmethod
    def post(cls, path):
        return cls(path, hdrs.METH_POST)
