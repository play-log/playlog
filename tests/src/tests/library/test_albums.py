import pytest

from tests.client import get
from tests.fixtures import fixture


def get_list(expected_status=200, **params):
    return get('albums', expected_status=expected_status, **params)


@fixture('albums')
def test_albums():
    # Offset, Limit
    data = get_list(offset=0, limit=2)
    assert len(data['items']) == 2
    assert data['total'] == 8

    # Filter by artist
    data = get_list(artist='amp', offset=0, limit=100)
    items = data['items']
    assert data['total'] == len(items) == 1
    assert items[0] == {
        'id': 8,
        'artist_id': 2,
        'name': 'Wading Through Rancid Offal',
        'artist': 'Amputated',
        'first_play': '2012-12-05T17:01:00',
        'last_play': '2012-12-05T17:22:00',
        'plays': 8
    }

    # Filter by name
    data = get_list(name='ga', offset=0, limit=100)
    items = data['items']
    assert len(items) == 2
    assert data['total'] == 2
    assert sorted([i['name'] for i in data['items']]) == sorted([
        'Organic Hallucinosis',
        'The Negation'
    ])

    # Filter by first play
    data = get_list(
        first_play_gt='2017-07-01T00:00',
        first_play_lt='2017-08-01T00:00',
        offset=0,
        limit=100
    )
    items = data['items']
    assert len(items) == 1
    assert data['total'] == 1
    assert items[0]['name'] == 'Anticult'

    # Filter by last play
    data = get_list(
        last_play_gt='2017-12-05T21:00',
        last_play_lt='2017-12-05T21:30',
        offset=0,
        limit=100
    )
    items = data['items']
    assert len(items) == 1
    assert data['total'] == 1
    assert items[0]['name'] == 'Nihility'

    # Order by plays
    data = get_list(order='-plays', offset=0, limit=5)
    items = data['items']
    assert len(items) == 5
    assert data['total'] == 8
    for c, n in zip(items, items[1:]):
        assert c['plays'] >= n['plays']


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
        'order': [
            "Value must be one of "
            "('artist', 'name', 'first_play', 'last_play', 'plays')."
        ]
    }),
    # too big limit
    ({'offset': 0, 'limit': 1000}, {'limit': ['Int value should be less than or equal to 100.']}),
    # too small limit
    ({'offset': 0, 'limit': 0}, {'limit': ['Int value should be greater than or equal to 1.']}),
])
def test_invalid_params(params, errors):
    assert errors == get_list(expected_status=400, **params)['errors']
