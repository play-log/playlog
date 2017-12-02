from requests import get

from tests.submissions import TestCase, get_session_id


class TestSubmissionsHandshake(TestCase):
    def test_handshake_greeting(self):
        rep = get(self.url('submissions/'))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'Audioscrobbler submissions system')
        self.assertIsNone(get_session_id())

    def test_handshake_failed_with_incorrect_protocol_version(self):
        rep = get(self.url('submissions/', hs='true', p='incorrect'))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'FAILED Incorrect protocol version')
        self.assertIsNone(get_session_id())

    def test_handshake_failed_with_unknown_username(self):
        rep = get(self.url('submissions/', hs='true', p='1.2', u='unknown'))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'BADAUTH')
        self.assertIsNone(get_session_id())

    def test_handshake_failed_with_invalid_timestamp(self):
        params = {'hs': 'true', 'p': '1.2', 'u': self.SUBMISSIONS_USERNAME, 't': 'invalid'}
        rep = get(self.url('submissions/', **params))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'FAILED Bad timestamp')
        self.assertIsNone(get_session_id())

    def test_handshake_failed_with_timeout(self):
        params = {'hs': 'true', 'p': '1.2', 'u': self.SUBMISSIONS_USERNAME, 't': '0'}
        rep = get(self.url('submissions/', **params))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'FAILED Bad timestamp')
        self.assertIsNone(get_session_id())

    def test_handshale_failed_with_invalid_token(self):
        timestamp = self.get_current_timestamp()
        rep = get(self.url('submissions/', **{
            'hs': 'true',
            'p': '1.2',
            'u': self.SUBMISSIONS_USERNAME,
            't': timestamp,
            'a': 'invalid'
        }))
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'BADAUTH')
        self.assertIsNone(get_session_id())

    def test_handshake_succeeded(self):
        self.perform_handshake()
