from schema import Optional

from playlog.decorators import route, with_query
from playlog.models import play
from playlog.lib.validation import Int, ISODateTime, Length, OneOf
from playlog.views import View


@route('/plays')
class Plays(View):
    @with_query({
        'offset': Int(min_val=0),
        'limit': Int(min_val=1, max_val=100),
        Optional('order_direction'): OneOf(play.ORDER_DIRECTIONS),
        Optional('order_field'): OneOf(play.ORDER_FIELDS),
        Optional('artist_name'): Length(min_len=1, max_len=50),
        Optional('album_name'): Length(min_len=1, max_len=50),
        Optional('track_name'): Length(min_len=1, max_len=50),
        Optional('date_lt'): ISODateTime(),
        Optional('date_gt'): ISODateTime()
    })
    async def get(self, query):
        async with self.db as conn:
            return self.json(await play.find_many(conn, **query))
