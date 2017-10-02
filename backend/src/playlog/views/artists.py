from playlog.decorators import route
from playlog.actions import artist, album, play


@route.get('/artists')
async def find_many(request):
    async with request.app['db'].acquire() as conn:
        return await artist.find_many(conn, dict(request.query))


@route.get('/artists/{id:\d+}')
async def find_one(request):
    async with request.app['db'].acquire() as conn:
        artist_id = request.match_info['id']
        data = dict(await artist.find_one(conn, id=artist_id))
        data['albums'] = await album.find_for_artist(conn, artist_id)
        data['years'] = await play.count_per_year_for_artist(conn, artist_id)
        return data
