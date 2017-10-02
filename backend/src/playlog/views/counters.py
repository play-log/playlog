from playlog.decorators import route
from playlog.actions import artist, album, track, play


@route.get('/counters')
async def counters(request):
    async with request.app['db'].acquire() as conn:
        return {
            'artists': await artist.count_total(conn),
            'albums': await album.count_total(conn),
            'tracks': await track.count_total(conn),
            'plays': await play.count_total(conn)
        }
