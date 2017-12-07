from requests import get

from tests import TestCase, db


class TestTracks(TestCase):
    def get_list(self, expected_status=200, **params):
        rep = get(self.url('tracks', **params))
        self.assertEqual(rep.status_code, expected_status, rep.text)
        return rep.json()

    def get_list_failed(self, **params):
        return self.get_list(expected_status=400, **params)

    def test_tracks_with_data(self):
        total = len(db.data['track'])

        # Offset, Limit
        data = self.get_list(offset=0, limit=2)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['total'], total)
        for item in data['items']:
            self.assertIn(item['id'], db.data['track'])
            self.assertEqual(item.pop('artist'), db.data['artist'][item.pop('artist_id')]['name'])
            self.assertEqual(item.pop('album'), db.data['album'][item['album_id']]['name'])
            self.assertEqual(item, db.data['track'][item['id']])

        # Filter by artist
        data = self.get_list(artist='ster', offset=0, limit=100)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Introduction')

        # Filter by album
        data = self.get_list(album='Einsamkeit', offset=0, limit=100)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Introduction')

        # Filter by track
        data = self.get_list(track='sh', offset=0, limit=100)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['total'], 2)
        self.assertEqual(sorted([i['name'] for i in data['items']]), sorted([
            'Extinguished Light',
            'Shrines Of Paralysis'
        ]))

        # Filter by first play
        data = self.get_list(
            first_play_gt='2016-10-24T10:36',
            first_play_lt='2016-10-24T10:38',
            offset=0,
            limit=100
        )
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Yield To Naught')

        # Filter by last_play
        data = self.get_list(
            last_play_gt='2017-08-31T14:24',
            last_play_lt='2017-08-31T14:26',
            offset=0,
            limit=100
        )
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'There Are No Saviours')

        # Order by plays
        data = self.get_list(
            order_field='plays',
            order_direction='desc',
            offset=0,
            limit=5
        )
        self.assertEqual(len(data['items']), 5)
        self.assertEqual(data['total'], total)
        for idx, track_id in enumerate([1, 2, 3, 4, 5]):
            track = data['items'][idx]
            self.assertEqual(track.pop('artist_id'), 1)
            self.assertEqual(track.pop('artist'), 'Ulcerate')
            self.assertEqual(track.pop('album'), 'Shrines Of Paralysis')
            self.assertEqual(track, db.data['track'][track_id])
        for c, n in zip(data['items'], data['items'][1:]):
            self.assertGreaterEqual(c['plays'], n['plays'])

        # Order by track
        items = self.get_list(
            order_field='track',
            order_direction='desc',
            offset=0,
            limit=100
        )['items']
        self.assertEqual(items[0]['name'], 'Yield To Naught')
        self.assertEqual(items[-1]['name'], 'Abrogation')

        # Order by album
        items = self.get_list(
            order_field='album',
            order_direction='asc',
            offset=0,
            limit=100
        )['items']
        self.assertEqual(items[0]['album'], 'Einsamkeit')
        self.assertEqual(items[-1]['album'], 'Shrines Of Paralysis')

    def test_tracks_without_data(self):
        self.assertEqual(
            self.get_list(offset=0, limit=100),
            {'items': [], 'total': 0}
        )

    def test_tracks_invalid_params(self):
        for params, message in [
            # Missing required
            ({}, "Missing keys: 'limit', 'offset'"),
            # Got extra
            ({'extra': 'param', 'offset': 0, 'limit': 1}, (
                "Wrong keys 'extra' in "
                "{'extra': 'param', 'offset': '0', 'limit': '1'}"
            )),
            # Too small artist
            ({'artist': '', 'offset': 0, 'limit': 1}, 'Length must be greater than 1'),
            # Too big artist
            ({'artist': 'a' * 51, 'offset': 0, 'limit': 1}, 'Length must be less than 50'),
            # Too small album
            ({'album': '', 'offset': 0, 'limit': 1}, 'Length must be greater than 1'),
            # Too big album
            ({'album': 'a' * 51, 'offset': 0, 'limit': 1}, 'Length must be less than 50'),
            # Too small track
            ({'track': '', 'offset': 0, 'limit': 1}, 'Length must be greater than 1'),
            # Too big track
            ({'track': 'a' * 51, 'offset': 0, 'limit': 1}, 'Length must be less than 50'),
            # first_play_lt is not a date
            ({'first_play_lt': 'w', 'offset': 0, 'limit': 1}, 'w is not a valid date'),
            # first_play_gt is not a date
            ({'first_play_gt': 'x', 'offset': 0, 'limit': 1}, 'x is not a valid date'),
            # last_play_lt is not a date
            ({'last_play_lt': 'y', 'offset': 0, 'limit': 1}, 'y is not a valid date'),
            # last_play_gt is not a date
            ({'last_play_gt': 'z', 'offset': 0, 'limit': 1}, 'z is not a valid date'),
            # order_field is not allowed
            ({'order_field': '__dict__', 'offset': 0, 'limit': 1}, (
                "__dict__ is not one of "
                "['artist', 'album', 'track', 'first_play', 'last_play', 'plays']"
            )),
            # order_direction is not allowed
            ({'order_direction': 'backward', 'offset': 0, 'limit': 1}, (
                "backward is not one of ['asc', 'desc']"
            )),
            # too big limit
            ({'offset': 0, 'limit': 1000}, '1000 is greater than 100'),
            # too small limit
            ({'offset': 0, 'limit': 0}, '0 is less than 1'),
        ]:
            self.assertIn(message, self.get_list_failed(**params))

    def test_track_found(self):
        rep = get(self.url('tracks/1'))
        self.assertEqual(rep.status_code, 200, rep.text)
        data = rep.json()
        plays = data.pop('plays')
        self.assertEqual(data, {
            'id': 1,
            'artist_id': 1,
            'artist_name': 'Ulcerate',
            'album_id': 1,
            'album_name': 'Shrines Of Paralysis',
            'name': 'Extinguished Light',
            'first_play': '2016-10-24T11:23:00',
            'last_play': '2017-08-31T15:07:00',
            'total_plays': 70
        })
        self.assertEqual(len(plays), 2)
        self.assertEqual(plays[0], {'track_id': 1, 'date': '2016-10-24T11:23:00'})
        self.assertEqual(plays[1], {'track_id': 1, 'date': '2017-08-31T15:07:00'})

    def test_track_not_found(self):
        rep = get(self.url('tracks/1'))
        self.assertEqual(rep.status_code, 404, rep.text)
        data = rep.json()
        self.assertEqual(data, {"message": "Not Found"})
