from requests import get

from tests import TestCase, db


class TestArtists(TestCase):
    def get_list(self, expected_status=200, **params):
        rep = get(self.url('artists', **params))
        self.assertEqual(rep.status_code, expected_status, rep.text)
        return rep.json()

    def get_list_failed(self, **params):
        return self.get_list(expected_status=400, **params)

    def test_artists_with_data(self):
        # Offset, Limit
        total = len(db.data['artist'])
        data = self.get_list(offset=0, limit=10)
        self.assertEqual(len(data['items']), 10)
        self.assertEqual(data['total'], total)
        self.assertEqual(data['items'][0], db.data['artist'][1])
        self.assertEqual(data['items'][-1], db.data['artist'][10])
        data = self.get_list(offset=10, limit=1)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0], db.data['artist'][11])
        self.assertEqual(data['total'], total)

        # Filter by name
        data = self.get_list(name='Ul', offset=0, limit=100)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['total'], 2)
        self.assertEqual([i['name'] for i in data['items']], ['Ulcerate', 'Ulsect'])

        # Filter by first play
        data = self.get_list(
            first_play_gt='2012-01-01T00:00',
            first_play_lt='2012-12-31T23:59',
            offset=0,
            limit=100
        )
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], '1349')

        # Filter by last_play
        data = self.get_list(
            last_play_gt='2017-11-14T00:00',
            last_play_lt='2017-11-15T00:00',
            offset=0,
            limit=100
        )
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Archspire')

        # Order by plays
        data = self.get_list(
            order_field='plays',
            order_direction='desc',
            offset=0,
            limit=5
        )
        self.assertEqual(len(data['items']), 5)
        self.assertEqual(data['total'], total)
        for idx, artist_id in enumerate([4, 29, 27, 1, 25]):
            self.assertEqual(data['items'][idx], db.data['artist'][artist_id])
        for c, n in zip(data['items'], data['items'][1:]):
            self.assertGreaterEqual(c['plays'], n['plays'])

    def test_artists_without_data(self):
        rep = get(self.url('artists', offset=0, limit=10))
        self.assertEqual(rep.status_code, 200, rep.text)
        data = rep.json()
        self.assertEqual(data, {'items': [], 'total': 0})

    def test_artists_invalid_params(self):
        for params, message in [
            # Missing required
            ({}, "Missing keys: 'limit', 'offset'"),
            # Got extra
            ({'extra': 'param', 'offset': 0, 'limit': 1}, (
                "Wrong keys 'extra' in "
                "{'extra': 'param', 'offset': '0', 'limit': '1'}"
            )),
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
                "__dict__ is not one of ['name', 'first_play', 'last_play', 'plays']"
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

    def test_artist_found(self):
        rep = get(self.url('artists/1'))
        self.assertEqual(rep.status_code, 200, rep.text)
        data = rep.json()
        albums = data.pop('albums')
        self.assertEqual(data, {
            'first_play': '2017-09-30T00:00:00',
            'last_play': '2017-09-30T00:00:00',
            'id': 1,
            'name': 'Immolation',
            'plays': 1
        })
        self.assertEqual(len(albums), 12)
        self.assertEqual(albums[0], {
            'artist_id': 1,
            'id': 12,
            'name': 'Atonement',
            'first_play': '2017-09-30T00:00:00',
            'last_play': '2017-10-30T00:00:00',
            'plays': 26
        })

    def test_artist_not_found(self):
        rep = get(self.url('artists/1'))
        self.assertEqual(rep.status_code, 404, rep.text)
        data = rep.json()
        self.assertEqual(data, {"message": "Not Found"})
