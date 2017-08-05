from playlog import gravatar
from playlog.config import USER_EMAIL, USER_NAME
from playlog.decorators import route
from playlog.views import View


@route('/overview')
class Overview(View):
    async def get(self):
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
                'artists': 23,
                'albums': 75,
                'tracks': 823,
                'plays': 4506,
                'favorites': 200
            },
            'years': [
                {'label': '2012', 'value': 13250},
                {'label': '2013', 'value': 14232},
                {'label': '2014', 'value': 17230},
                {'label': '2015', 'value': 22351},
                {'label': '2016', 'value': 21347},
                {'label': '2017', 'value': 8346},
            ],
            'recent_tracks': [
                {
                    'artist': 'Epitimia',
                    'album': 'Four Truths Of The Noble Ones',
                    'track': 'Nirvana',
                    'date': '2017-07-01T02:18:00',
                    'is_favorite': False,
                },
                {
                    'artist': 'Epitimia',
                    'album': 'Four Truths Of The Noble Ones',
                    'track': 'The Path To The End Of Suffering - I Aspire Like A Bird',
                    'date': '2017-07-01T02:13:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': 'Four Truths Of The Noble Ones',
                    'track': 'Suffering\'s Cessation - Moksha',
                    'date': '2017-07-01T02:06:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': 'Four Truths Of The Noble Ones',
                    'track': 'Suffering\'s Origin - To The Sorrowful',
                    'date': '2017-07-01T01:53:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': 'Four Truths Of The Noble Ones',
                    'track': 'The Nature Of Suffering - Waiting For The Doom',
                    'date': '2017-07-01T01:47:00',
                    'is_favorite': True
                },
                {
                    'artist': 'Epitimia',
                    'album': 'Four Truths Of The Noble Ones',
                    'track': 'Satori',
                    'date': '2017-07-01T01:44:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Rebirth',
                    'date': '2017-06-30T00:47:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion VII - Catharsis',
                    'date': '2017-06-30T00:37:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion VI - Fracture',
                    'date': '2017-06-30T00:32:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion V - Far Away',
                    'date': '2017-06-30T00:26:00',
                    'is_favorite': True
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion IV - Reflection',
                    'date': '2017-06-30T00:20:00',
                    'is_favorite': True
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion III - Foretime',
                    'date': '2017-06-30T00:15:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion II - Oath',
                    'date': '2017-06-30T00:08:00',
                    'is_favorite': False
                },
                {
                    'artist': 'Epitimia',
                    'album': '(Un)reality',
                    'track': 'Illusion I - Muse',
                    'date': '2017-06-30T00:01:00',
                    'is_favorite': False
                }
            ]
        })
