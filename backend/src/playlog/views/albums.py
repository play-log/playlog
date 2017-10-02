from playlog.actions import album, track, play
from playlog.decorators import autowired, route


@route.get('/albums')
@autowired
async def find_many(request, db):
    return await album.find_many(db, dict(request.query))


@route.get('/albums/{id:\d+}')
@autowired
async def find_one(request, db):
    album_id = request.match_info['id']
    data = dict(await album.find_one(db, id=album_id))
    data['tracks'] = await track.find_for_album(db, album_id)
    data['years'] = await play.count_per_year_for_album(db, album_id)
    return data
