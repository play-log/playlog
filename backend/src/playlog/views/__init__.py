from aiohttp.web import View as BaseView, json_response


class View(BaseView):
    @property
    def db(self):
        return self.request.app['db'].acquire()

    json = staticmethod(json_response)
