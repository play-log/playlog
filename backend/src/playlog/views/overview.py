from datetime import datetime, timedelta

from playlog.lib import gravatar
from playlog.config import USER_EMAIL, USER_NAME
from playlog.decorators import autowired, route
from playlog.actions import artist, album, track, play


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


@route.get('/overview')
@autowired
async def overview(request, db):
    return {
        'current_streak': await play.get_current_streak(db),
        'longest_streak': await play.get_longest_streak(db),
        'biggest_day': await play.get_biggest_day(db),
        'recently_added': await get_recently_added(db),
        'user': {
            'avatar_src': gravatar.get_url(USER_EMAIL, size=64),
            'name': USER_NAME,
            'listening_since': await play.get_listening_since(db)
        },
        'nowplay': await request.app['nowplay'].get(),
        'counters': {
            'artists': await artist.count_total(db),
            'albums': await album.count_total(db),
            'tracks': await track.count_total(db),
            'plays': await play.count_total(db)
        },
        'years': await play.count_per_year(db),
        'recent_tracks': await play.get_recent(db)
    }
