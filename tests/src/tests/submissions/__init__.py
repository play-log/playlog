from hashlib import md5
from time import time

from tests.client import BASE_URL

NOWPLAY_URL = '{}/submissions/nowplay'.format(BASE_URL)
SUBMIT_URL = '{}/submissions/submit'.format(BASE_URL)
USERNAME = 'fabien'
PASSWORD_HASH = '81dc9bdb52d04dc20036dbd8313ed055'


def get_current_timestamp():
    return str(int(time()))


def generate_token(timestamp):
    token = md5(PASSWORD_HASH.encode('utf-8'))
    token.update(timestamp.encode('utf-8'))
    return token.hexdigest()
