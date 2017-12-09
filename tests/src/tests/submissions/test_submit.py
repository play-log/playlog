from datetime import datetime, timedelta

from requests import post

from tests.client import get
from tests.fixtures import fixture, refresh_db
from tests.submissions import SUBMIT_URL


def test_submit_one_success(perform_handshake):
    refresh_db()
    session_id, _, submit_url = perform_handshake()
    date = datetime(2017, 11, 25, 14, 58)
    iso_date = date.isoformat()
    rep = post(submit_url, data={
        'a[0]': 'Fleshgod Apocalypse',
        'b[0]': 'Labyrinth',
        't[0]': 'Prologue',
        'i[0]': str(int(date.timestamp())),
        's': session_id
    })
    assert rep.status_code == 200, rep.text
    assert rep.text == 'OK'

    artist = get('artists/1')
    assert artist['id'] == 1
    assert artist['name'] == 'Fleshgod Apocalypse'
    assert artist['plays'] == 1
    assert iso_date == artist['first_play'] == artist['last_play']

    album = get('albums/1')
    assert album['id'] == 1
    assert album['artist_id'] == 1
    assert album['name'] == 'Labyrinth'
    assert album['plays'] == 1
    assert iso_date == album['first_play'] == album['last_play']

    track = get('tracks/1')
    assert track['id'] == 1
    assert track['album_id'] == 1
    assert track['name'] == 'Prologue'
    assert track['total_plays'] == 1
    assert iso_date == track['first_play'] == track['last_play']

    plays = get('plays', offset=0, limit=100)
    assert len(plays['items']) == 1 == plays['total']
    play = plays['items'][0]
    assert play['track_id'] == 1
    assert play['date'] == iso_date


@fixture('submit-many')
def test_submit_many_success(perform_handshake):
    date = datetime(2017, 11, 25, 16, 21)
    session_id, _, submit_url = perform_handshake()
    rep = post(submit_url, data={
        # Submit existing track
        'a[0]': 'Test',
        'b[0]': 'Test',
        't[0]': 'Test',
        'i[0]': str(int((date + timedelta(minutes=10)).timestamp())),
        # Submit new track for existing album and artist
        'a[1]': 'Test',
        'b[1]': 'Test',
        't[1]': 'Test new track',
        'i[1]': str(int((date + timedelta(minutes=20)).timestamp())),
        # Submit new album and track for existing artist
        'a[2]': 'Test',
        'b[2]': 'Test new album',
        't[2]': 'Test new track',
        'i[2]': str(int((date + timedelta(minutes=30)).timestamp())),
        # Submit new artist
        'a[3]': 'Test new artist',
        'b[3]': 'Test',
        't[3]': 'Test',
        'i[3]': str(int((date + timedelta(minutes=40)).timestamp())),
        # Session
        's': session_id
    })
    assert rep.status_code == 200, rep.text
    assert rep.text == 'OK'

    artists = get('artists', offset=0, limit=100)
    assert len(artists['items']) == 2 == artists['total']
    items = sorted(artists['items'], key=lambda i: i['id'])
    assert items[0] == {
        'id': 1,
        'name': 'Test',
        'plays': 4,
        'first_play': date.isoformat(),
        'last_play': (date + timedelta(minutes=30)).isoformat()
    }
    assert items[1] == {
        'id': 2,
        'name': 'Test new artist',
        'plays': 1,
        'first_play': (date + timedelta(minutes=40)).isoformat(),
        'last_play': (date + timedelta(minutes=40)).isoformat(),
    }

    albums = get('albums', offset=0, limit=100)
    assert len(albums['items']) == 3 == albums['total']
    items = sorted(albums['items'], key=lambda i: i['id'])
    assert items[0] == {
        'id': 1,
        'artist_id': 1,
        'artist': 'Test',
        'name': 'Test',
        'plays': 3,
        'first_play': date.isoformat(),
        'last_play': (date + timedelta(minutes=20)).isoformat()
    }
    assert items[1] == {
        'id': 2,
        'artist_id': 1,
        'artist': 'Test',
        'name': 'Test new album',
        'plays': 1,
        'first_play': (date + timedelta(minutes=30)).isoformat(),
        'last_play': (date + timedelta(minutes=30)).isoformat()
    }
    assert items[2] == {
        'id': 3,
        'artist_id': 2,
        'artist': 'Test new artist',
        'name': 'Test',
        'plays': 1,
        'first_play': (date + timedelta(minutes=40)).isoformat(),
        'last_play': (date + timedelta(minutes=40)).isoformat()
    }

    tracks = get('tracks', offset=0, limit=100)
    assert len(tracks['items']) == 4 == tracks['total']
    items = sorted(tracks['items'], key=lambda i: i['id'])
    assert items[0] == {
        'id': 1,
        'artist_id': 1,
        'artist': 'Test',
        'album_id': 1,
        'album': 'Test',
        'name': 'Test',
        'plays': 2,
        'first_play': date.isoformat(),
        'last_play': (date + timedelta(minutes=10)).isoformat()
    }
    assert items[1] == {
        'id': 2,
        'artist_id': 1,
        'artist': 'Test',
        'album_id': 1,
        'album': 'Test',
        'name': 'Test new track',
        'plays': 1,
        'first_play': (date + timedelta(minutes=20)).isoformat(),
        'last_play': (date + timedelta(minutes=20)).isoformat()
    }
    assert items[2] == {
        'id': 3,
        'artist_id': 1,
        'artist': 'Test',
        'album_id': 2,
        'album': 'Test new album',
        'name': 'Test new track',
        'plays': 1,
        'first_play': (date + timedelta(minutes=30)).isoformat(),
        'last_play': (date + timedelta(minutes=30)).isoformat()
    }
    assert items[3] == {
        'id': 4,
        'artist_id': 2,
        'artist': 'Test new artist',
        'album_id': 3,
        'album': 'Test',
        'name': 'Test',
        'plays': 1,
        'first_play': (date + timedelta(minutes=40)).isoformat(),
        'last_play': (date + timedelta(minutes=40)).isoformat()
    }


def test_submit_many_exceeded(perform_handshake):
    refresh_db()
    keys = ['a', 'b', 't']
    data = {}
    for i in range(100):
        value = 'Test {}'.format(i)
        for k in keys:
            data['{}[{}]'.format(k, i)] = value
        data['i[{}]'.format(i)] = i

    session_id, _, submit_url = perform_handshake()
    data['s'] = session_id
    rep = post(submit_url, data=data)
    assert rep.status_code == 200, rep.text
    assert rep.text == 'OK'
    assert get('counters') == {
        'artists': 50,
        'albums': 50,
        'tracks': 50,
        'plays': 50
    }


def test_submit_failed_without_session_id():
    rep = post(SUBMIT_URL, data={})
    assert rep.status_code == 200, rep.text
    assert rep.text == 'BADSESSION'


def test_submit_failed_with_bad_session_id(perform_handshake):
    session_id, _, submit_url = perform_handshake()
    rep = post(submit_url, data={'s': 'invalid-session-id'})
    assert rep.status_code == 200, rep.text
    assert rep.text == 'BADSESSION'


def test_submit_failed_with_invalid_data(perform_handshake):
    session_id, _, submit_url = perform_handshake()
    dataset = [
        {},
        {'a[0]': 'Without', 'b[0]': 'Title', 'i[0]': '0'},
        {'a[0]': 'Without', 't[0]': 'Album', 'i[0]': '0'},
        {'b[0]': 'Without', 't[0]': 'Artist', 'i[0]': '0'},
        {'a[0]': 'Without', 'b[0]': 'Timestamp', 't[0]': 'Test'},
        {'a[0]': '', 'b[0]': 'With Empty', 't[0]': 'Artist', 'i[0]': '0'},
        {'a[0]': 'With Empty', 'b[0]': '', 't[0]': 'Album', 'i[0]': '0'},
        {'a[0]': 'With Empty', 'b[0]': 'Track', 't[0]': '', 'i[0]': '0'},
        {'a[0]': 'With', 'b[0]': 'Empty', 't[0]': 'Timestamp', 'i[0]': ''},
        {'a[0]': 'With', 'b[0]': 'Invalid', 't[0]': 'Timestamp', 'i[0]': 'xxx'}
    ]
    for data in dataset:
        rep = post(submit_url, data={**data, 's': session_id})
        assert rep.status_code == 200, rep.text
        assert rep.text == 'OK'
        assert get('counters') == {
            'artists': 50,
            'albums': 50,
            'tracks': 50,
            'plays': 50
        }


@fixture('submit-existing')
def test_submit_existing_date_failed(perform_handshake):
    date = datetime(2017, 11, 25, 15, 55)
    iso_date = date.isoformat()
    session_id, _, submit_url = perform_handshake()
    rep = post(submit_url, data={
        'a[0]': 'Test',
        'b[0]': 'Test',
        't[0]': 'Test',
        'i[0]': str(int(date.timestamp())),
        's': session_id
    })
    assert rep.status_code == 200, rep.text
    assert rep.text == 'OK'

    for key in ('artists', 'albums', 'tracks'):
        data = get(key, offset=0, limit=100)
        assert len(data['items']) == 1 == data['total']
        item = data['items'][0]
        assert item['plays'] == 1
        assert item['first_play'] == iso_date == item['last_play']
    plays = get('plays', offset=0, limit=100)
    assert len(plays['items']) == 1 == plays['total']
    play = plays['items'][0]
    assert play['track_id'] == 1
    assert play['date'] == iso_date
