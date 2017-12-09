from tests.client import get
from tests.fixtures import fixture


@fixture('artist')
def test_artist_found():
    data = get('artists/1')
    albums = data.pop('albums')
    assert data == {
        'first_play': '2017-09-30T00:00:00',
        'last_play': '2017-09-30T00:00:00',
        'id': 1,
        'name': 'Immolation',
        'plays': 1
    }
    assert len(albums) == 12
    assert albums[0] == {
        'artist_id': 1,
        'id': 1,
        'name': 'Dawn Of Posession',
        'first_play': '2017-09-30T00:00:00',
        'last_play': '2017-09-30T00:00:00',
        'plays': 1
    }


def test_artist_not_found():
    assert get('artists/1', expected_status=404) == {"message": "Not Found"}
