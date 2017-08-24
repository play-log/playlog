import functools

import aiohttp.web
import venusian

from schema import Schema, SchemaError


def route(path):
    def decorator(view):
        if not issubclass(view, aiohttp.web.View):
            raise TypeError('Expects subclass of aiohttp.web.View')

        def callback(scanner, name, ob):
            scanner.router.add_route('*', path, view)
        venusian.attach(view, callback)
        return view

    return decorator


def with_query(definition):
    schema = Schema(definition)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args):
            try:
                query = schema.validate(dict(self.request.query))
            except SchemaError as exc:
                result = self.json([i for i in exc.autos if i is not None], status=400)
            else:
                result = await func(self, query)
            return result
        return wrapper
    return decorator
