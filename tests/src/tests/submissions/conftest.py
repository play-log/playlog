import pytest

from requests import get

from tests.client import url
from tests.submissions import (
    NOWPLAY_URL,
    SUBMIT_URL,
    USERNAME,
    generate_token,
    get_current_timestamp
)


@pytest.fixture
def perform_handshake(get_session_id):
    def wrapper():
        timestamp = get_current_timestamp()
        rep = get(url('submissions/', **{
            'hs': 'true',
            'p': '1.2',
            'u': USERNAME,
            't': timestamp,
            'a': generate_token(timestamp)
        }))
        assert rep.status_code == 200, rep.text
        parts = rep.text.split('\n')
        assert len(parts) == 4, rep.text
        status, session_id, nowplay_url, submit_url = parts
        assert status == 'OK'
        assert session_id == get_session_id()
        assert nowplay_url == NOWPLAY_URL
        assert submit_url == SUBMIT_URL
        return session_id, nowplay_url, submit_url
    return wrapper
