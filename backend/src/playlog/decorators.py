import aiohttp.web
import venusian


def route(path):
    def decorator(view):
        if not issubclass(view, aiohttp.web.View):
            raise TypeError('Expects subclass of aiohttp.web.View')

        def callback(scanner, name, ob):
            scanner.router.add_route('*', path, view)
        venusian.attach(view, callback)
        return view

    return decorator
