from playlog.decorators import route
from playlog.actions import track, play
from playlog.views import View


@route('/tracks')
class Tracks(View):
    async def get(self):
        async with self.db as conn:
            return await track.find_many(conn, dict(self.request.query))


@route('/tracks/{id:\d+}')
class Track(View):
    async def get(self):
        async with self.db as conn:
            track_id = self.request.match_info['id']
            data = dict(await track.find_one(conn, id=track_id))
            data['total_plays'] = data.pop('plays')
            data['plays'] = await play.find_for_track(conn, track_id)
            data['years'] = await play.count_per_year_for_track(conn, track_id)
            return data
