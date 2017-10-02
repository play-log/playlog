import venusian

from aiohttp import hdrs


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
