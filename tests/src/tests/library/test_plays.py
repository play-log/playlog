from datetime import datetime

import pytest

from tests.client import get
from tests.fixtures import fixture


def get_list(expected_status=200, **params):
    return get('plays', expected_status=expected_status, **params)


@fixture('plays')
def test_default_params():
    data = get_list(offset=0, limit=10)
    assert data['total'] == 33
    assert len(data['items']) == 10
    for item in data['items']:
        assert item['artist'] == 'Ulcerate'
        assert item['album'] == 'Shrines Of Paralysis'
        assert item['track'] == 'Extinguished Light'
        item['date'] = datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S')
    for curr_item, next_item in zip(data['items'], data['items'][1:]):
        assert curr_item['date'] >= next_item['date']


@fixture('plays')
def test_filters():
    # Artist filter
    data = get_list(artist='ster', offset=0, limit=10)
    assert data['total'] == 1
    assert len(data['items']) == 1
    assert data['items'][0]['artist'] == 'Sterbend'

    # Album filter
    data = get_list(album='shri', offset=0, limit=10)
    assert data['total'] == 32
    assert len(data['items']) == 10
    assert all(i['album'] == 'Shrines Of Paralysis' for i in data['items'])

    # Track filter
    data = get_list(track='intro', offset=0, limit=10)
    assert data['total'] == 1
    assert len(data['items']) == 1
    assert data['items'][0]['track'] == 'Introduction'

    # Date filter
    data = get_list(date_gt='2017-08-01T00:00', date_lt='2017-09-01T00:00', offset=0, limit=20)
    assert data['total'] == 17
    assert len(data['items']) == 17
    assert all('2017-08-' in i['date'] for i in data['items'])


@fixture('plays')
@pytest.mark.parametrize('field,first,last', [
    ('artist', 'Sterbend', 'Ulcerate'),
    ('album', 'Einsamkeit', 'Shrines Of Paralysis'),
    ('track', 'Extinguished Light', 'Introduction'),
    ('date', 'Introduction', 'Extinguished Light')
])
def test_order(field, first, last):
    for direction in ['asc', 'desc']:
        items = get_list(
            order_field=field,
            order_direction=direction,
            offset=0,
            limit=50
        )['items']
        msg = 'Unexpected order: field={} direction={}'.format(field, direction)
        cmp_field = 'track' if field == 'date' else field
        if direction == 'desc':
            first, last = last, first
        assert items[0][cmp_field] == first, msg
        assert items[-1][cmp_field] == last, msg


def test_empty_db():
    assert get_list(offset=0, limit=100) == {'items': [], 'total': 0}


@pytest.mark.parametrize('params,errors', [
    # Missing required
    ({}, {'limit': ['This field is required.'], 'offset': ['This field is required.']}),
    # Got extra
    ({'extra': 'param', 'offset': 0, 'limit': 1}, {'extra': 'Rogue field'}),
    # Too small artist
    ({'artist': '', 'offset': 0, 'limit': 1}, {'artist': ['String value is too short.']}),
    # Too big artist
    ({'artist': 'a' * 51, 'offset': 0, 'limit': 1}, {'artist': ['String value is too long.']}),
    # Too small album
    ({'album': '', 'offset': 0, 'limit': 1}, {'album': ['String value is too short.']}),
    # Too big album
    ({'album': 'a' * 51, 'offset': 0, 'limit': 1}, {'album': ['String value is too long.']}),
    # Too small track
    ({'track': '', 'offset': 0, 'limit': 1}, {'track': ['String value is too short.']}),
    # Too big track
    ({'track': 'a' * 51, 'offset': 0, 'limit': 1}, {'track': ['String value is too long.']}),
    # date_lt is not a date
    ({'date_lt': 'w', 'offset': 0, 'limit': 1}, {'date_lt': [
        'Could not parse w. Should be ISO 8601 or timestamp.']
    }),
    # date_gt is not a date
    ({'date_gt': 'x', 'offset': 0, 'limit': 1},  {
        'date_gt': ['Could not parse x. Should be ISO 8601 or timestamp.']
    }),
    # order_field is not allowed
    ({'order_field': '__dict__', 'offset': 0, 'limit': 1}, {
        'order_field': [
            "Value must be one of "
            "['artist', 'album', 'track', 'date']."
        ]
    }),
    # order_direction is not allowed
    ({'order_direction': 'backward', 'offset': 0, 'limit': 1}, {
        'order_direction': ["Value must be one of ['asc', 'desc']."]
    }),
    # too big limit
    ({'offset': 0, 'limit': 1000}, {'limit': ['Int value should be less than or equal to 100.']}),
    # too small limit
    ({'offset': 0, 'limit': 0}, {'limit': ['Int value should be greater than or equal to 1.']}),
])
def test_invalid_params(params, errors):
    assert errors == get_list(expected_status=400, **params)['errors']
