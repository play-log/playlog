from requests import get

from tests import TestCase, db


class TestCounters(TestCase):
    def test_counters_without_data(self):
        rep = get(self.url('counters'))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.json(), {
            'artists': 0,
            'albums': 0,
            'tracks': 0,
            'plays': 0
        })

    def test_counters_with_data(self):
        rep = get(self.url('counters'))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.json(), {
            'artists': len(db.data['artist']),
            'albums': len(db.data['album']),
            'tracks': len(db.data['track']),
            'plays': len(db.data['play'])
        })
