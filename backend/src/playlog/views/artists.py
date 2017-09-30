from playlog.decorators import route
from playlog.actions import artist, album, play
from playlog.views import View


@route('/artists')
class Artists(View):
    async def get(self):
        async with self.db as conn:
            return self.json(await artist.find_many(conn, dict(self.request.query)))


@route('/artists/{id:\d+}')
class Artist(View):
    async def get(self):
        async with self.db as conn:
            artist_id = self.request.match_info['id']
            data = dict(await artist.find_one(conn, id=artist_id))
            data['albums'] = await album.find_for_artist(conn, artist_id)
            data['years'] = await play.count_per_year_for_artist(conn, artist_id)
            return self.json(data)
