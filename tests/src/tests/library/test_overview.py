from datetime import date, timedelta

from tests.client import get
from tests.fixtures import fixture


def get_data():
    return get('overview')


AVATAR_SRC = 'http://www.gravatar.com/avatar/9a22d09f92d50fa3d2a16766d0ba52f8?s=64'
USER_NAME = 'Fabien Potencier'


def test_without_data():
    today = date.today().isoformat()
    month_ago = (date.today() - timedelta(days=30)).isoformat()

    data = get_data()

    current_streak = data.pop('current_streak')
    assert today in current_streak.pop('start_date')
    assert today in current_streak.pop('end_date')
    assert current_streak == {
        'days': 0.0,
        'plays': 0
    }

    assert data.pop('longest_streak') is None

    assert data.pop('biggest_day') is None

    recently_added = data.pop('recently_added')
    assert month_ago in recently_added.pop('start_date')
    assert today in recently_added.pop('end_date')
    assert recently_added == {
        'artists': 0,
        'albums': 0,
        'tracks': 0,
    }

    assert data.pop('user') == {
        'avatar_src': AVATAR_SRC,
        'name': USER_NAME,
        'listening_since': None
    }

    assert data.pop('nowplay') is None

    assert data.pop('counters') == {
        'artists': 0,
        'albums': 0,
        'tracks': 0,
        'plays': 0
    }

    assert data.pop('recent_tracks') == []

    assert not data


@fixture('overview')
def test_with_data():
    today = date.today().isoformat()
    month_ago = (date.today() - timedelta(days=30)).isoformat()

    data = get_data()

    current_streak = data.pop('current_streak')
    assert today in current_streak.pop('start_date')
    assert today in current_streak.pop('end_date')
    assert current_streak == {
        'days': 0.0,
        'plays': 0
    }

    assert data.pop('longest_streak') == {
        'start_date': '2017-01-02T00:00:00',
        'end_date': '2017-01-04T00:00:00',
        'days': 2,
        'plays': 46
    }

    assert data.pop('biggest_day') == {
        'day': '2017-01-04T00:00:00',
        'plays': 36
    }

    recently_added = data.pop('recently_added')
    assert month_ago in recently_added.pop('start_date')
    assert today in recently_added.pop('end_date')
    assert recently_added == {
        'artists': 0,
        'albums': 0,
        'tracks': 0,
    }

    assert data.pop('user') == {
        'avatar_src': AVATAR_SRC,
        'name': USER_NAME,
        'listening_since': 2017
    }

    assert data.pop('nowplay') is None

    assert data.pop('counters') == {
        'artists': 1,
        'albums': 1,
        'tracks': 10,
        'plays': 46
    }

    recent_tracks = data.pop('recent_tracks')
    assert len(recent_tracks) == 15
    assert recent_tracks[0] == {
        'artist': 'Analepsy',
        'artist_id': 1,
        'album': 'Atrocities From Beyond',
        'album_id': 1,
        'track': 'Omen Of Return (Instrumental)',
        'track_id': 10,
        'date': '2017-01-04T11:29:13.497261'
    }

    assert not data


def test_with_nowplay(set_current_track):
    track = {
        'artist': 'Analepsy',
        'album': 'Atrocities From Beyond',
        'title': 'Eons In Vacuum'
    }
    set_current_track(**track)
    data = get_data()
    assert data['nowplay'] == track
