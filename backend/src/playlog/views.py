from aiohttp.web import View, json_response as json

from .decorators import route


@route('/')
class Index(View):
    async def get(self):
        return json({'hello': 'world'})


@route('/overview')
class Overview(View):
    async def get(self):
        return json({
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
                'avatar_src': 'https://gravatar.com/avatar/4e3d9780ddadc53333ae1541ea48eaf4?s=64',
                'name': 'Ross Nomann',
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
                # TODO: group tracks by date on frontend, use isoformat for time
                {
                    'date': 'July 01, 2017',
                    'items': [
                        {'is_favorite': False, 'data': 'Epitimia — Four Truths Of The Noble Ones — Nirvana', 'time': '02:18'},
                        {'is_favorite': False, 'data': 'Epitimia — Four Truths Of The Noble Ones — The Path To The End Of Suffering - I Aspire Like A Bird', 'time': '02:13'},
                        {'is_favorite': False, 'data': 'Epitimia — Four Truths Of The Noble Ones — Suffering\'s Cessation - Moksha', 'time': '02:06'},
                        {'is_favorite': False, 'data': 'Epitimia — Four Truths Of The Noble Ones — Suffering\'s Origin - To The Sorrowful', 'time': '01:53'},
                        {'is_favorite': True, 'data': 'Epitimia — Four Truths Of The Noble Ones — The Nature Of Suffering - Waiting For The Doom', 'time': '01:47'},
                        {'is_favorite': False, 'data': 'Epitimia — Four Truths Of The Noble Ones — Satori', 'time': '01:44'},
                    ]
                },
                {
                    'date': 'June 30, 2017',
                    'items': [
                        {'is_favorite': False, 'data': 'Epitimia — (Un)reality — Rebirth', 'time': '00:47'},
                        {'is_favorite': False, 'data': 'Epitimia — (Un)reality — Illusion VII - Catharsis', 'time': '00:37'},
                        {'is_favorite': False, 'data': 'Epitimia — (Un)reality — Illusion VI - Fracture', 'time': '00:32'},
                        {'is_favorite': True, 'data': 'Epitimia — (Un)reality — Illusion V - Far Away', 'time': '00:26'},
                        {'is_favorite': True, 'data': 'Epitimia — (Un)reality — Illusion IV - Reflection', 'time': '00:20'},
                        {'is_favorite': False, 'data': 'Epitimia — (Un)reality — Illusion III - Foretime', 'time': '00:15'},
                        {'is_favorite': False, 'data': 'Epitimia — (Un)reality — Illusion II - Oath', 'time': '00:08'},
                        {'is_favorite': False, 'data': 'Epitimia — (Un)reality — Illusion I - Muse', 'time': '00:01'}
                    ]
                }
            ]
        })
