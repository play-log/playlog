from playlog import gravatar
from playlog.config import USER_EMAIL, USER_NAME
from playlog.decorators import route
from playlog.models import artist, album, track, play
from playlog.views import View


@route('/overview')
class Overview(View):
    async def get(self):
        async with self.db as conn:
            return self.json({
                'current_streak': {
                    'days': 19,
                    'plays': 678,
                    'start_date': '2017-06-05T00:00:00',
                    'end_date': '2017-06-24T00:00:00'
                },
                'longest_streak': {
                    'days': 30,
                    'plays': 1563,
                    'start_date': '2017-05-01T00:00:00',
                    'end_date': '2017-05-30T00:00:00'
                },
                'biggest_day': {
                    'plays': 132,
                    'date': '2017-05-30T00:00:00'
                },
                'recently_added': {
                    'artists': 8,
                    'albums': 24,
                    'tracks': 317,
                    'start_date': '2017-06-01T00:00:00',
                    'end_date': '2017-06-25T00:00:00'
                },
                'user': {
                    'avatar_src': gravatar.get_url(USER_EMAIL, size=64),
                    'name': USER_NAME,
                    'listening_since': '2012'
                },
                'nowplay': {
                    'artist': 'Epitimia',
                    'album': 'Faces Of Insanity',
                    'title': 'Epikrisis I - Altered State Of Consciousness'
                },
                'counters': {
                    'artists': await artist.count_total(conn),
                    'albums': await album.count_total(conn),
                    'tracks': await track.count_total(conn),
                    'plays': await play.count_total(conn),
                    'favorites': await track.count_favorite(conn)
                },
                'years': [
                    {'label': '2012', 'value': 13250},
                    {'label': '2013', 'value': 14232},
                    {'label': '2014', 'value': 17230},
                    {'label': '2015', 'value': 22351},
                    {'label': '2016', 'value': 21347},
                    {'label': '2017', 'value': 8346},
                ],
                'recent_tracks': await play.get_recent(conn)
            })
