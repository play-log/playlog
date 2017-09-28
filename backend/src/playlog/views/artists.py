from schema import Optional

from playlog.decorators import route, with_query
from playlog.actions import artist, album, play
from playlog.lib.validation import Int, ISODateTime, Length, OneOf
from playlog.views import View


@route('/artists')
class Artists(View):
    @with_query({
        'offset': Int(min_val=0),
        'limit': Int(min_val=1, max_val=100),
        Optional('order_direction'): OneOf(artist.ORDER_DIRECTIONS),
        Optional('order_field'): OneOf(artist.ORDER_FIELDS),
        Optional('name'): Length(min_len=1, max_len=50),
        Optional('first_play_lt'): ISODateTime(),
        Optional('first_play_gt'): ISODateTime(),
        Optional('last_play_lt'): ISODateTime(),
        Optional('last_play_gt'): ISODateTime(),
    })
    async def get(self, query):
        async with self.db as conn:
            return self.json(await artist.find_many(conn, **query))


@route('/artists/{id:\d+}')
class Artist(View):
    async def get(self):
        async with self.db as conn:
            artist_id = self.request.match_info['id']
            data = dict(await artist.find_one(conn, id=artist_id))
            data['albums'] = await album.find_for_artist(conn, artist_id)
            data['years'] = await play.count_per_year_for_artist(conn, artist_id)
            return self.json(data)
