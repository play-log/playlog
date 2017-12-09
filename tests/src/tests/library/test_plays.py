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


@pytest.mark.parametrize('params,message', [
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
])
def test_invalid_params(params, message):
    assert message in get_list(expected_status=400, **params)
