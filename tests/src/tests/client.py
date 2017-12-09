import requests

from urllib.parse import urlencode

__all__ = ['get', 'url']

BASE_URL = 'http://127.0.0.1:8080'


def url(path, **params):
    return '{}/{}?{}'.format(BASE_URL, path, urlencode(params))


def get(path, expected_status=200, **params):
    rep = requests.get(url(path, **params))
    assert rep.status_code == expected_status, rep.text
    return rep.json()
