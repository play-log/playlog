from requests import get

from tests import TestCase, db


class TestAlbums(TestCase):
    def get_list(self, expected_status=200, **params):
        rep = get(self.url('albums', **params))
        self.assertEqual(rep.status_code, expected_status, rep.text)
        return rep.json()

    def get_list_failed(self, **params):
        return self.get_list(expected_status=400, **params)

    def test_albums_with_data(self):
        total = len(db.data['album'])

        # Offset, Limit
        data = self.get_list(offset=0, limit=2)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['total'], total)
        for item in data['items']:
            self.assertIn(item['id'], db.data['album'])
            self.assertEqual(item.pop('artist'), db.data['artist'][item['artist_id']]['name'])
            self.assertEqual(item, db.data['album'][item['id']])

        # Filter by artist
        data = self.get_list(artist='amp', offset=0, limit=100)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Wading Through Rancid Offal')

        # Filter by name
        data = self.get_list(name='ga', offset=0, limit=100)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['total'], 2)
        self.assertEqual(sorted([i['name'] for i in data['items']]), sorted([
            'Organic Hallucinosis',
            'The Negation'
        ]))

        # Filter by first play
        data = self.get_list(
            first_play_gt='2017-07-01T00:00',
            first_play_lt='2017-08-01T00:00',
            offset=0,
            limit=100
        )
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Anticult')

        # Filter by last_play
        data = self.get_list(
            last_play_gt='2017-12-05T21:00',
            last_play_lt='2017-12-05T21:30',
            offset=0,
            limit=100
        )
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Nihility')

        # Order by plays
        data = self.get_list(
            order_field='plays',
            order_direction='desc',
            offset=0,
            limit=5
        )
        self.assertEqual(len(data['items']), 5)
        self.assertEqual(data['total'], total)
        for idx, album_id in enumerate([3, 7, 2, 6, 4]):
            self.assertEqual(data['items'][idx].pop('artist'), 'Decapitated')
            self.assertEqual(data['items'][idx], db.data['album'][album_id])
        for c, n in zip(data['items'], data['items'][1:]):
            self.assertGreaterEqual(c['plays'], n['plays'])

    def test_albums_without_data(self):
        self.assertEqual(
            self.get_list(offset=0, limit=100),
            {'items': [], 'total': 0}
        )

    def test_albums_invalid_params(self):
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
            # Too small name
            ({'name': '', 'offset': 0, 'limit': 1}, 'Length must be greater than 1'),
            # Too big name
            ({'name': 'a' * 51, 'offset': 0, 'limit': 1}, 'Length must be less than 50'),
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
                "__dict__ is not one of ['artist', 'name', 'first_play', 'last_play', 'plays']"
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

    def test_album_found(self):
        rep = get(self.url('albums/1'))
        self.assertEqual(rep.status_code, 200, rep.text)
        data = rep.json()
        tracks = data.pop('tracks')
        self.assertEqual(data, {
            'id': 1,
            'artist_id': 1,
            'artist_name': 'Decapitated',
            'name': 'Winds Of Creation',
            'first_play': '2014-02-09T13:37:00',
            'last_play': '2017-12-04T12:29:00',
            'plays': 144
        })
        self.assertEqual(len(tracks), 9)
        self.assertEqual(tracks[0], {
            'id': 1,
            'album_id': 1,
            'name': 'Winds Of Creation',
            'first_play': '2014-08-22T18:07:00',
            'last_play': '2017-12-04T11:46:00',
            'plays': 16
        })

    def test_album_not_found(self):
        rep = get(self.url('albums/1'))
        self.assertEqual(rep.status_code, 404, rep.text)
        data = rep.json()
        self.assertEqual(data, {"message": "Not Found"})
