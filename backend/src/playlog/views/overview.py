from datetime import datetime, timedelta

from playlog import gravatar
from playlog.config import USER_EMAIL, USER_NAME
from playlog.decorators import route
from playlog.models import artist, album, track, play
from playlog.views import View


async def get_recently_added(conn):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    return {
        'artists': await artist.count_new(conn, start_date),
        'albums': await album.count_new(conn, start_date),
        'tracks': await track.count_new(conn, start_date),
        'start_date': start_date,
        'end_date': end_date
    }


@route('/overview')
class Overview(View):
    async def get(self):
        async with self.db as conn:
            return self.json({
                'current_streak': await play.get_current_streak(conn),
                'longest_streak': await play.get_longest_streak(conn),
                'biggest_day': await play.get_biggest_day(conn),
                'recently_added': await get_recently_added(conn),
                'user': {
                    'avatar_src': gravatar.get_url(USER_EMAIL, size=64),
                    'name': USER_NAME,
                    'listening_since': await play.get_listening_since(conn)
                },
                'nowplay': await self.nowplay.get(),
                'counters': {
                    'artists': await artist.count_total(conn),
                    'albums': await album.count_total(conn),
                    'tracks': await track.count_total(conn),
                    'plays': await play.count_total(conn)
                },
                'years': await play.count_per_year(conn),
                'recent_tracks': await play.get_recent(conn)
            })
