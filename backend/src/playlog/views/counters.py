from playlog.decorators import route
from playlog.models import artist, album, track, play
from playlog.views import View


@route('/counters')
class Counters(View):
    async def get(self):
        async with self.db as conn:
            return self.json({
                'artists': await artist.count_total(conn),
                'albums': await album.count_total(conn),
                'tracks': await track.count_total(conn),
                'plays': await play.count_total(conn),
                'favorites': await track.count_favorite(conn)
            })
