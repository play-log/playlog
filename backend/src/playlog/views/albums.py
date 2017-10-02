from playlog.actions import album, track, play
from playlog.decorators import route


@route.get('/albums')
async def find_many(request):
    async with request.app['db'].acquire() as conn:
        return await album.find_many(conn, dict(request.query))


@route.get('/albums/{id:\d+}')
async def find_one(request):
    async with request.app['db'].acquire() as conn:
        album_id = request.match_info['id']
        data = dict(await album.find_one(conn, id=album_id))
        data['tracks'] = await track.find_for_album(conn, album_id)
        data['years'] = await play.count_per_year_for_album(conn, album_id)
        return data
