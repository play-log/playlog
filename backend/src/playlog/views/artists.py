from schema import Optional

from playlog.decorators import route, with_query
from playlog.models import artist
from playlog.validation import Int, ISODateTime, Length, OneOf
from playlog.views import View


@route('/artists')
class Artists(View):
    @with_query({
        'offset': Int(min_val=0),
        'limit': Int(min_val=1),
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
