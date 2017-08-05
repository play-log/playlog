from aiohttp.web import View as BaseView, json_response


class View(BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    json = staticmethod(json_response)
