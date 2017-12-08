from datetime import datetime

from requests import get

from tests import TestCase


class TestPlays(TestCase):
    def get_list(self, expected_status=200, **params):
        rep = get(self.url('plays'), params=params)
        self.assertEqual(rep.status_code, expected_status, rep.text)
        return rep.json()

    def get_list_failed(self, **params):
        return self.get_list(expected_status=400, **params)

    def get_count(self, expected_status=200, **params):
        rep = get(self.url('plays/count'), params=params)
        self.assertEqual(rep.status_code, expected_status, rep.text)
        return rep.json()

    def assert_default_list(self):
        data = self.get_list(offset=0, limit=10)
        self.assertEqual(data['total'], 33)
        self.assertEqual(len(data['items']), 10)
        for item in data['items']:
            self.assertEqual(item['artist'], 'Ulcerate')
            self.assertEqual(item['album'], 'Shrines Of Paralysis')
            self.assertEqual(item['track'], 'Extinguished Light')
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S')
        for curr_item, next_item in zip(data['items'], data['items'][1:]):
            self.assertGreaterEqual(curr_item['date'], next_item['date'])

    def assert_artist_filter_works(self):
        data = self.get_list(artist='ster', offset=0, limit=10)
        self.assertEqual(data['total'], 1)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['artist'], 'Sterbend')

    def assert_album_filter_works(self):
        data = self.get_list(album='shri', offset=0, limit=10)
        self.assertEqual(data['total'], 32)
        self.assertEqual(len(data['items']), 10)
        self.assertTrue(all(i['album'] == 'Shrines Of Paralysis' for i in data['items']))

    def assert_track_filter_works(self):
        data = self.get_list(track='intro', offset=0, limit=10)
        self.assertEqual(data['total'], 1)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['track'], 'Introduction')

    def assert_date_filter_works(self):
        data = self.get_list(
            date_gt='2017-08-01T00:00',
            date_lt='2017-09-01T00:00',
            offset=0,
            limit=20
        )
        self.assertEqual(data['total'], 17)
        self.assertEqual(len(data['items']), 17)
        self.assertTrue(all('2017-08-' in i['date'] for i in data['items']))

    def assert_order_works(self):
        for field, first, last in [
            ('artist', 'Sterbend', 'Ulcerate'),
            ('album', 'Einsamkeit', 'Shrines Of Paralysis'),
            ('track', 'Extinguished Light', 'Introduction'),
            ('date', 'Introduction', 'Extinguished Light')
        ]:
            for direction in ['asc', 'desc']:
                items = self.get_list(
                    order_field=field,
                    order_direction=direction,
                    offset=0,
                    limit=50
                )['items']
                msg = 'Unexpected order: field={} direction={}'.format(field, direction)
                cmp_field = 'track' if field == 'date' else field
                if direction == 'desc':
                    first, last = last, first
                self.assertEqual(items[0][cmp_field], first, msg)
                self.assertEqual(items[-1][cmp_field], last, msg)

    def assert_default_count(self):
        self.assertEqual(self.get_count(), [
            {'label': '2012-01-01T00:00:00', 'value': 1},
            {'label': '2016-01-01T00:00:00', 'value': 1},
            {'label': '2017-01-01T00:00:00', 'value': 31}
        ])

    def assert_count_empty_period(self):
        self.assertEqual(self.get_count(period=''), [
            {'label': '2012-01-01T00:00:00', 'value': 1},
            {'label': '2016-01-01T00:00:00', 'value': 1},
            {'label': '2017-01-01T00:00:00', 'value': 31}
        ])

    def assert_month_count(self):
        self.assertEqual(self.get_count(period=2017), [
            {'label': '2017-02-01T00:00:00', 'value': 1},
            {'label': '2017-03-01T00:00:00', 'value': 12},
            {'label': '2017-05-01T00:00:00', 'value': 1},
            {'label': '2017-08-01T00:00:00', 'value': 17}
        ])

    def assert_day_count(self):
        self.assertEqual(self.get_count(period='2017-08'), [
            {'label': '2017-08-01T00:00:00', 'value': 1},
            {'label': '2017-08-06T00:00:00', 'value': 4},
            {'label': '2017-08-10T00:00:00', 'value': 1},
            {'label': '2017-08-18T00:00:00', 'value': 1},
            {'label': '2017-08-21T00:00:00', 'value': 1},
            {'label': '2017-08-22T00:00:00', 'value': 1},
            {'label': '2017-08-23T00:00:00', 'value': 1},
            {'label': '2017-08-25T00:00:00', 'value': 1},
            {'label': '2017-08-28T00:00:00', 'value': 1},
            {'label': '2017-08-29T00:00:00', 'value': 2},
            {'label': '2017-08-30T00:00:00', 'value': 1},
            {'label': '2017-08-31T00:00:00', 'value': 2}
        ])

    def assert_hour_count(self):
        self.assertEqual(self.get_count(period='2017-08-06'), [
            {'label': '2017-08-06T01:00:00', 'value': 2},
            {'label': '2017-08-06T21:00:00', 'value': 2}
        ])

    def assert_artist_count(self):
        data = self.get_count(filter_kind='artist', filter_value=1, period='2017-08-06')
        self.assertEqual(data, [
            {'label': '2017-08-06T01:00:00', 'value': 2},
            {'label': '2017-08-06T21:00:00', 'value': 2}
        ])

    def assert_album_count(self):
        data = self.get_count(filter_kind='album', filter_value=2)
        self.assertEqual(data, [{'label': '2012-01-01T00:00:00', 'value': 1}])

    def assert_track_count(self):
        data = self.get_count(filter_kind='track', filter_value=2)
        self.assertEqual(data, [{'label': '2012-01-01T00:00:00', 'value': 1}])

    def test_with_data(self):
        self.assert_default_list()
        self.assert_artist_filter_works()
        self.assert_album_filter_works()
        self.assert_track_filter_works()
        self.assert_date_filter_works()
        self.assert_order_works()

        self.assert_default_count()
        self.assert_count_empty_period()
        self.assert_month_count()
        self.assert_day_count()
        self.assert_hour_count()
        self.assert_artist_count()
        self.assert_album_count()
        self.assert_track_count()

    def test_without_data(self):
        self.assertEqual(self.get_list(offset=0, limit=10), {'items': [], 'total': 0})
        self.assertEqual(self.get_count(), [])

    def test_invalid_params(self):
        for params, message in [
            ({'extra': 'param'}, "Wrong keys 'extra' in {'extra': 'param'}"),
            ({'period': 'x'}, 'Invalid period: x'),
            ({'period': '0-0-0-0-0-0'}, 'Invalid period: 0-0-0-0-0-0'),
            ({'period': '1-1-1-1-1-1'}, 'Invalid period: 1-1-1-1-1-1'),
            ({'period': '2012-0100-0110'}, 'Invalid period: 2012-0100-0110'),
            ({'filter_kind': '__dict__'}, "__dict__ is not one of ['artist', 'album', 'track']"),
            ({'filter_value': 'x'}, 'x is not an integer'),
            # TODO: should return 400
            ({'filter_kind': 'artist'}, (500, 'message'))
        ]:
            if len(message) == 2:
                status, message = message
            else:
                status = 400
            self.assertIn(message, self.get_count(expected_status=status, **params))

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
            # date_lt is not a date
            ({'date_lt': 'w', 'offset': 0, 'limit': 1}, 'w is not a valid date'),
            # date_gt is not a date
            ({'date_gt': 'x', 'offset': 0, 'limit': 1}, 'x is not a valid date'),
            # order_field is not allowed
            ({'order_field': '__dict__', 'offset': 0, 'limit': 1}, (
                "__dict__ is not one of "
                "['artist', 'album', 'track', 'date']"
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
