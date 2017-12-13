import pytest

from tests.client import get
from tests.fixtures import fixture


def get_list(expected_status=200, **params):
    return get('artists', expected_status=expected_status, **params)


@fixture('artists')
def test_artists():
    # Offset, Limit
    data = get_list(offset=0, limit=2)
    assert len(data['items']) == 2
    assert data['total'] == 102

    # Filter by name
    data = get_list(name='ul', offset=0, limit=100)
    items = data['items']
    assert len(items) == 2
    assert data['total'] == 2
    assert sorted([i['name'] for i in data['items']]) == sorted([
        'Ulcerate',
        'Ulsect'
    ])

    # Filter by first play
    data = get_list(
        first_play_gt='2012-01-01T00:00',
        first_play_lt='2012-12-31T23:59',
        offset=0,
        limit=100
    )
    items = data['items']
    assert len(items) == 1
    assert data['total'] == 1
    assert items[0]['name'] == '1349'

    # Filter by last play
    data = get_list(
        last_play_gt='2017-11-14T00:00',
        last_play_lt='2017-11-15T00:00',
        offset=0,
        limit=100
    )
    items = data['items']
    assert len(items) == 1
    assert data['total'] == 1
    assert items[0]['name'] == 'Archspire'

    # Order by plays
    data = get_list(order='-plays', offset=0, limit=5)
    items = data['items']
    assert len(items) == 5
    assert data['total'] == 102
    for c, n in zip(items, items[1:]):
        assert c['plays'] >= n['plays']


def test_empty_db():
    assert get_list(offset=0, limit=100) == {'items': [], 'total': 0}


@pytest.mark.parametrize('params,errors', [
    # Missing required
    ({}, {'limit': ['This field is required.'], 'offset': ['This field is required.']}),
    # Got extra
    ({'extra': 'param', 'offset': 0, 'limit': 1}, {'extra': 'Rogue field'}),
    # Too small name
    ({'name': '', 'offset': 0, 'limit': 1}, {'name': ['String value is too short.']}),
    # Too big name
    ({'name': 'a' * 51, 'offset': 0, 'limit': 1}, {'name': ['String value is too long.']}),
    # first_play_lt is not a date
    ({'first_play_lt': 'w', 'offset': 0, 'limit': 1}, {
        'first_play_lt': ['Could not parse w. Should be ISO 8601 or timestamp.']
    }),
    # first_play_gt is not a date
    ({'first_play_gt': 'x', 'offset': 0, 'limit': 1},  {
        'first_play_gt': ['Could not parse x. Should be ISO 8601 or timestamp.']
    }),
    # last_play_lt is not a date
    ({'last_play_lt': 'y', 'offset': 0, 'limit': 1}, {'last_play_lt': [
        'Could not parse y. Should be ISO 8601 or timestamp.']
    }),
    # last_play_gt is not a date
    ({'last_play_gt': 'z', 'offset': 0, 'limit': 1}, {
        'last_play_gt': ['Could not parse z. Should be ISO 8601 or timestamp.']
    }),
    # order is not allowed
    ({'order': '__dict__', 'offset': 0, 'limit': 1}, {
        'order': ["Value must be one of ('name', 'first_play', 'last_play', 'plays')."]
    }),
    # too big limit
    ({'offset': 0, 'limit': 1000}, {'limit': ['Int value should be less than or equal to 100.']}),
    # too small limit
    ({'offset': 0, 'limit': 0}, {'limit': ['Int value should be greater than or equal to 1.']}),
])
def test_invalid_params(params, errors):
    assert errors == get_list(expected_status=400, **params)['errors']
