from playlog.decorators import route
from playlog.views import View


@route('/counters')
class Counters(View):
    async def get(self):
        return self.json({
            'artists': 23,
            'albums': 75,
            'tracks': 823,
            'plays': 4506,
            'favorites': 200
        })
