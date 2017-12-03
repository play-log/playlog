from datetime import date, timedelta

from requests import get

from tests import TestCase, set_current_track


AVATAR_SRC = 'http://www.gravatar.com/avatar/9a22d09f92d50fa3d2a16766d0ba52f8?s=64'
USER_NAME = 'Fabien Potencier'


class TestOverview(TestCase):
    def test_overview_without_data(self):
        today = date.today().isoformat()
        month_ago = (date.today() - timedelta(days=30)).isoformat()

        rep = get(self.url('overview'))
        self.assertEqual(rep.status_code, 200, rep.text)

        data = rep.json()

        current_streak = data.pop('current_streak')
        self.assertIn(today, current_streak.pop('start_date'))
        self.assertIn(today, current_streak.pop('end_date'))
        self.assertEqual(current_streak, {
            'days': 0.0,
            'plays': 0
        })

        self.assertIsNone(data.pop('longest_streak'))

        self.assertIsNone(data.pop('biggest_day'))

        recently_added = data.pop('recently_added')
        self.assertIn(month_ago, recently_added.pop('start_date'))
        self.assertIn(today, recently_added.pop('end_date'))
        self.assertEqual(recently_added, {
            'artists': 0,
            'albums': 0,
            'tracks': 0,
        })

        self.assertEqual(data.pop('user'), {
            'avatar_src': AVATAR_SRC,
            'name': USER_NAME,
            'listening_since': None
        })

        self.assertIsNone(data.pop('nowplay'))

        self.assertEqual(data.pop('counters'), {
            'artists': 0,
            'albums': 0,
            'tracks': 0,
            'plays': 0
        })

        self.assertEqual(data.pop('recent_tracks'), [])

        self.assertFalse(data)

    def test_overview_with_data(self):
        today = date.today().isoformat()
        month_ago = (date.today() - timedelta(days=30)).isoformat()

        rep = get(self.url('overview'))
        self.assertEqual(rep.status_code, 200, rep.text)

        data = rep.json()

        current_streak = data.pop('current_streak')
        self.assertIn(today, current_streak.pop('start_date'))
        self.assertIn(today, current_streak.pop('end_date'))
        self.assertEqual(current_streak, {
            'days': 0.0,
            'plays': 0
        })

        self.assertEqual(data.pop('longest_streak'), {
            'start_date': '2017-01-02T00:00:00',
            'end_date': '2017-01-04T00:00:00',
            'days': 2,
            'plays': 46
        })

        self.assertEqual(data.pop('biggest_day'), {
            'day': '2017-01-04T00:00:00',
            'plays': 36
        })

        recently_added = data.pop('recently_added')
        self.assertIn(month_ago, recently_added.pop('start_date'))
        self.assertIn(today, recently_added.pop('end_date'))
        self.assertEqual(recently_added, {
            'artists': 0,
            'albums': 0,
            'tracks': 0,
        })

        self.assertEqual(data.pop('user'), {
            'avatar_src': AVATAR_SRC,
            'name': USER_NAME,
            'listening_since': 2017
        })

        self.assertIsNone(data.pop('nowplay'))

        self.assertEqual(data.pop('counters'), {
            'artists': 1,
            'albums': 1,
            'tracks': 10,
            'plays': 46
        })

        recent_tracks = data.pop('recent_tracks')
        self.assertEqual(len(recent_tracks), 15)
        self.assertEqual(recent_tracks[0], {
            'artist': 'Analepsy',
            'artist_id': 1,
            'album': 'Atrocities From Beyond',
            'album_id': 1,
            'track': 'Omen Of Return (Instrumental)',
            'track_id': 10,
            'date': '2017-01-04T11:29:13.497261'
        })

        self.assertFalse(data)

    def test_overview_with_nowplay(self):
        track = {
            'artist': 'Analepsy',
            'album': 'Atrocities From Beyond',
            'title': 'Eons In Vacuum'
        }
        set_current_track(**track)
        rep = get(self.url('overview'))
        self.assertEqual(rep.status_code, 200, rep.text)
        data = rep.json()
        self.assertEqual(data['nowplay'], track)
