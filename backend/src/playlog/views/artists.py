from playlog.decorators import autowired, route
from playlog.actions import artist, album, play


@route.get('/artists')
@autowired
async def find_many(request, db):
    return await artist.find_many(db, dict(request.query))


@route.get('/artists/{id:\d+}')
@autowired
async def find_one(request, db):
    artist_id = request.match_info['id']
    data = dict(await artist.find_one(db, id=artist_id))
    data['albums'] = await album.find_for_artist(db, artist_id)
    data['years'] = await play.count_per_year_for_artist(db, artist_id)
    return data
