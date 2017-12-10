from requests import get

from tests.client import url
from tests.fixtures import refresh_db


def test_unknown_accept_header():
    refresh_db()
    rep = get(url('overview'), headers={'Accept': 'text/xml'})
    assert rep.status_code == 400, rep.text
