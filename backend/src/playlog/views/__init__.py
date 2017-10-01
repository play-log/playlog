from aiohttp.web import View as BaseView


class View(BaseView):
    def __getattr__(self, name):
        if name in self.request.app:
            return self.request.app[name]
        raise AttributeError('object %r has no attribute %s' % (self, name))

    @property
    def db(self):
        return self.request.app['db'].acquire()
