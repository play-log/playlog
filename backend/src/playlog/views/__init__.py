from functools import partial

from aiohttp.web import View as BaseView, json_response

from playlog.json import dumps as json_dumps


class View(BaseView):
    def __getattr__(self, name):
        if name in self.request.app:
            return self.request.app[name]
        raise AttributeError('object %r has no attribute %s' % (self, name))

    @property
    def db(self):
        return self.request.app['db'].acquire()

    json = staticmethod(partial(json_response, dumps=json_dumps))
