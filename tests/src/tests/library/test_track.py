from tests.client import get
from tests.fixtures import fixture


@fixture('track')
def test_found():
    data = get('tracks/1')
    plays = data.pop('plays')
    assert data == {
        'id': 1,
        'artist_id': 1,
        'artist_name': 'Ulcerate',
        'album_id': 1,
        'album_name': 'Shrines Of Paralysis',
        'name': 'Extinguished Light',
        'first_play': '2016-10-24T11:23:00',
        'last_play': '2017-08-31T15:07:00',
        'total_plays': 70
    }
    assert len(plays) == 2
    assert plays[0] == {'track_id': 1, 'date': '2016-10-24T11:23:00'}
    assert plays[1] == {'track_id': 1, 'date': '2017-08-31T15:07:00'}


def test_not_found():
    assert get('tracks/1', expected_status=404) == {"message": "Not Found"}
