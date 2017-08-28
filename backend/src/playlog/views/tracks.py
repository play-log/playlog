from schema import Optional

from playlog.decorators import route, with_query
from playlog.models import track
from playlog.validation import Int, ISODateTime, Length, OneOf
from playlog.views import View


@route('/tracks')
class Tracks(View):
    @with_query({
        'offset': Int(min_val=0),
        'limit': Int(min_val=1, max_val=100),
        Optional('order_direction'): OneOf(track.ORDER_DIRECTIONS),
        Optional('order_field'): OneOf(track.ORDER_FIELDS),
        Optional('artist_name'): Length(min_len=1, max_len=50),
        Optional('album_name'): Length(min_len=1, max_len=50),
        Optional('track_name'): Length(min_len=1, max_len=50),
        Optional('first_play_lt'): ISODateTime(),
        Optional('first_play_gt'): ISODateTime(),
        Optional('last_play_lt'): ISODateTime(),
        Optional('last_play_gt'): ISODateTime(),
    })
    async def get(self, query):
        async with self.db as conn:
            return self.json(await track.find_many(conn, **query))
