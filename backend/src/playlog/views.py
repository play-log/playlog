from aiohttp.web import View, json_response as json

from .decorators import route


@route('/')
class IndexView(View):
    async def get(self):
        return json({'hello': 'world'})
