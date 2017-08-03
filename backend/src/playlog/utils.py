import hashlib


GRAVATAR_URL = 'http://www.gravatar.com/avatar/'


def get_gravatar(email, *, size=None):
    url = GRAVATAR_URL + hashlib.md5(email.encode('utf-8')).hexdigest()
    if size:
        url = '{}?s={}'.format(url, str(size))
    return url
