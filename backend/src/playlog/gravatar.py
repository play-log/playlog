import hashlib


BASE_URL = 'http://www.gravatar.com/avatar/'


def get_url(email, *, size=None):
    url = BASE_URL + hashlib.md5(email.encode('utf-8')).hexdigest()
    if size:
        url = '{}?s={}'.format(url, str(size))
    return url
