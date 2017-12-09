from requests import get

from tests.client import url
from tests.submissions import USERNAME, get_current_timestamp


def send(**params):
    rep = get(url('submissions/', **params))
    assert rep.status_code == 200, rep.text
    return rep.text


def test_handshake_greeting(get_session_id):
    assert send() == 'Audioscrobbler submissions system'
    assert get_session_id() is None


def test_handshake_failed_with_incorrect_protocol_version(get_session_id):
    assert send(hs='true', p='incorrect') == 'FAILED Incorrect protocol version'
    assert get_session_id() is None


def test_handshake_failed_with_unknown_username(get_session_id):
    assert send(hs='true', p='1.2', u='unknown') == 'BADAUTH'
    assert get_session_id() is None


def test_handshake_failed_with_invalid_timestamp(get_session_id):
    params = {'hs': 'true', 'p': '1.2', 'u': USERNAME, 't': 'invalid'}
    assert send(**params) == 'FAILED Bad timestamp'
    assert get_session_id() is None


def test_handshake_failed_with_timeout(get_session_id):
    params = {'hs': 'true', 'p': '1.2', 'u': USERNAME, 't': '0'}
    assert send(**params) == 'FAILED Bad timestamp'
    assert get_session_id() is None


def test_handshale_failed_with_invalid_token(get_session_id):
    timestamp = get_current_timestamp()
    assert send(hs='true', p='1.2', u=USERNAME, t=timestamp, a='invalid') == 'BADAUTH'
    assert get_session_id() is None


def test_handshake_succeeded(get_session_id, perform_handshake):
    perform_handshake()
    assert get_session_id() is not None
