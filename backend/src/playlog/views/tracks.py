from playlog.decorators import route
from playlog.actions import track, play


@route.get('/tracks')
async def find_many(request):
    async with request.app['db'].acquire() as conn:
        return await track.find_many(conn, dict(request.query))


@route.get('/tracks/{id:\d+}')
async def find_one(request):
    async with request.app['db'].acquire() as conn:
        track_id = request.match_info['id']
        data = dict(await track.find_one(conn, id=track_id))
        data['total_plays'] = data.pop('plays')
        data['plays'] = await play.find_for_track(conn, track_id)
        data['years'] = await play.count_per_year_for_track(conn, track_id)
        return data
