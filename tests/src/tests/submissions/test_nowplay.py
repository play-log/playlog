from time import sleep

from requests import post

from tests.submissions import NOWPLAY_URL


def test_nowplay_success(perform_handshake, get_current_track):
    session_id, nowplay_url, _ = perform_handshake()
    data = {
        'a': 'Fleshgod Apocalypse',
        'b': 'Mafia',
        't': 'Conspiracy Of Silence',
        'l': '329',
        's': session_id
    }
    rep = post(nowplay_url, data=data)
    assert rep.status_code == 200, rep.text
    assert rep.text == 'OK'
    actual_track = get_current_track()
    assert actual_track is not None
    assert actual_track.pop('artist'), data['a']
    assert actual_track.pop('album'), data['b']
    assert actual_track.pop('title'), data['t']
    assert len(actual_track) == 0


def test_nowplay_expires(perform_handshake, get_current_track):
    session_id, nowplay_url, _ = perform_handshake()
    data = {
        'a': 'Unknown Artist',
        'b': 'Unknown Album',
        't': 'Unknown Track',
        'l': '2',
        's': session_id
    }
    rep = post(nowplay_url, data=data)
    assert rep.status_code == 200, rep.text
    assert rep.text == 'OK'
    actual_track = get_current_track()
    assert actual_track is not None
    assert actual_track.pop('artist') == data['a']
    assert actual_track.pop('album') == data['b']
    assert actual_track.pop('title') == data['t']
    assert len(actual_track) == 0
    # Unfortunately it is necessary
    # because track should expire after 2 seconds
    sleep(2)
    assert get_current_track() is None


def test_nowplay_failed_without_session_id(get_current_track):
    rep = post(NOWPLAY_URL, data={})
    assert rep.status_code == 200, rep.text
    assert rep.text == 'BADSESSION'
    assert get_current_track() is None


def test_nowplay_failed_with_bad_session_id(perform_handshake, get_current_track):
    _, nowplay_url, _ = perform_handshake()
    rep = post(nowplay_url, data={'s': 'invalid-session-id'})
    assert rep.status_code == 200, rep.text
    assert rep.text == 'BADSESSION'
    assert get_current_track() is None


def test_nowplay_failed_with_bad_data(perform_handshake, get_current_track):
    session_id, nowplay_url, _ = perform_handshake()
    dataset = [
        {'b': 'Without', 't': 'Artist', 'l': '329'},
        {'a': 'Without', 't': 'Album', 'l': '329'},
        {'a': 'Without', 'b': 'Title', 'l': '329'},
        {'a': 'Without', 'b': 'Length', 't': 'Test'},
        {'a': 'With', 'b': 'Invalid', 't': 'Length', 'l': 'invalid'},
        {'a': 'With', 'b': 'Empty', 't': 'Length', 'l': ''},
        {'a': '', 'b': 'With Empty', 't': 'Artist', 'l': '329'},
        {'a': 'With Empty', 'b': '', 't': 'Album', 'l': '329'},
        {'a': 'With', 'b': 'Empty Title', 't': '', 'l': '329'},
        {}
    ]
    for data in dataset:
        rep = post(nowplay_url, data={**data, 's': session_id})
        assert rep.status_code == 200, rep.text
        assert rep.text == 'OK'
        get_current_track() is None
