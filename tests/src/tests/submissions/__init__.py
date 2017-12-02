from hashlib import md5
from time import time

from requests import get

from tests import TestCase as BaseTestCase, get_session_id


class TestCase(BaseTestCase):
    SUBMISSIONS_NOWPLAY_URL = '{}/submissions/nowplay'.format(BaseTestCase.BASE_URL)
    SUBMISSIONS_SUBMIT_URL = '{}/submissions/submit'.format(BaseTestCase.BASE_URL)
    SUBMISSIONS_USERNAME = 'fabien'
    SUBMISSIONS_PASSWORD_HASH = '81dc9bdb52d04dc20036dbd8313ed055'

    def perform_handshake(self):
        timestamp = self.get_current_timestamp()
        rep = get(self.url('submissions/', **{
            'hs': 'true',
            'p': '1.2',
            'u': self.SUBMISSIONS_USERNAME,
            't': timestamp,
            'a': self.generate_token(timestamp)
        }))
        self.assertEqual(rep.status_code, 200, rep.text)
        parts = rep.text.split('\n')
        self.assertEqual(len(parts), 4, rep.text)
        status, session_id, nowplay_url, submit_url = parts
        self.assertEqual(status, 'OK')
        self.assertEqual(session_id, get_session_id())
        self.assertEqual(nowplay_url, self.SUBMISSIONS_NOWPLAY_URL)
        self.assertEqual(submit_url, self.SUBMISSIONS_SUBMIT_URL)
        return session_id, nowplay_url, submit_url

    def generate_token(self, timestamp):
        token = md5(self.SUBMISSIONS_PASSWORD_HASH.encode('utf-8'))
        token.update(timestamp.encode('utf-8'))
        return token.hexdigest()

    @staticmethod
    def get_current_timestamp():
        return str(int(time()))
