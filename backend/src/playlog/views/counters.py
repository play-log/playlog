from playlog.decorators import autowired, route
from playlog.actions import artist, album, track, play


@route.get('/counters')
@autowired
async def counters(request, db):
    return {
        'artists': await artist.count_total(db),
        'albums': await album.count_total(db),
        'tracks': await track.count_total(db),
        'plays': await play.count_total(db)
    }
