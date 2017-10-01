from playlog.decorators import route
from playlog.actions import album, track, play
from playlog.views import View


@route('/albums')
class Albums(View):
    async def get(self):
        async with self.db as conn:
            return await album.find_many(conn, dict(self.request.query))


@route('/albums/{id:\d+}')
class Album(View):
    async def get(self):
        async with self.db as conn:
            album_id = self.request.match_info['id']
            data = dict(await album.find_one(conn, id=album_id))
            data['tracks'] = await track.find_for_album(conn, album_id)
            data['years'] = await play.count_per_year_for_album(conn, album_id)
            return data
