from playlog.decorators import route
from playlog.actions import play
from playlog.views import View


@route('/plays')
class Plays(View):
    async def get(self):
        async with self.db as conn:
            return self.json(await play.find_many(conn, dict(self.request.query)))
