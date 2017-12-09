from requests import get

from tests.client import url


def test_unknown_accept_header():
    rep = get(url('overview'), headers={'Accept': 'text/xml'})
    assert rep.status_code == 400, rep.text
