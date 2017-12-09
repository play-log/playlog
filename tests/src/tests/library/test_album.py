from tests.client import get
from tests.fixtures import fixture


@fixture('album')
def test_found():
    data = get('albums/1')
    tracks = data.pop('tracks')
    assert data == {
        'id': 1,
        'artist_id': 1,
        'artist_name': 'Decapitated',
        'name': 'Winds Of Creation',
        'first_play': '2014-02-09T13:37:00',
        'last_play': '2017-12-04T12:29:00',
        'plays': 144
    }
    assert len(tracks) == 9
    assert tracks[0] == {
        'id': 1,
        'album_id': 1,
        'name': 'Winds Of Creation',
        'first_play': '2014-08-22T18:07:00',
        'last_play': '2017-12-04T11:46:00',
        'plays': 16
    }


def test_not_found():
    assert get('albums/1', expected_status=404) == {"message": "Not Found"}
