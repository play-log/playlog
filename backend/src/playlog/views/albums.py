from schema import Optional

from playlog.decorators import route, with_query
from playlog.actions import album, track, play
from playlog.lib.validation import Int, ISODateTime, Length, OneOf
from playlog.views import View


@route('/albums')
class Albums(View):
    @with_query({
        'offset': Int(min_val=0),
        'limit': Int(min_val=1, max_val=100),
        Optional('order_direction'): OneOf(album.ORDER_DIRECTIONS),
        Optional('order_field'): OneOf(album.ORDER_FIELDS),
        Optional('artist_name'): Length(min_len=1, max_len=50),
        Optional('album_name'): Length(min_len=1, max_len=50),
        Optional('first_play_lt'): ISODateTime(),
        Optional('first_play_gt'): ISODateTime(),
        Optional('last_play_lt'): ISODateTime(),
        Optional('last_play_gt'): ISODateTime(),
    })
    async def get(self, query):
        async with self.db as conn:
            return self.json(await album.find_many(conn, **query))


@route('/albums/{id:\d+}')
class Album(View):
    async def get(self):
        async with self.db as conn:
            album_id = self.request.match_info['id']
            data = dict(await album.find_one(conn, id=album_id))
            data['tracks'] = await track.find_for_album(conn, album_id)
            data['years'] = await play.count_per_year_for_album(conn, album_id)
            return self.json(data)
