from playlog.decorators import autowired, route
from playlog.actions import track, play


@route.get('/tracks')
@autowired
async def find_many(request, db):
    return await track.find_many(db, dict(request.query))


@route.get('/tracks/{id:\d+}')
@autowired
async def find_one(request, db):
    track_id = request.match_info['id']
    data = dict(await track.find_one(db, id=track_id))
    data['total_plays'] = data.pop('plays')
    data['plays'] = await play.find_for_track(db, track_id)
    data['years'] = await play.count_per_year_for_track(db, track_id)
    return data
