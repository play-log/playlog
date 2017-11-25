from time import sleep

from requests import post

from . import TestCase


class TestSubmissionsNowplay(TestCase):
    def test_nowplay_success(self):
        session_id, nowplay_url, _ = self.perform_handshake()
        data = {
            'a': 'Fleshgod Apocalypse',
            'b': 'Mafia',
            't': 'Conspiracy Of Silence',
            'l': '329',
            's': session_id
        }
        rep = post(nowplay_url, data=data)
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'OK')
        actual_track = self.get_current_track()
        self.assertIsNotNone(actual_track)
        self.assertEqual(actual_track.pop('artist'), data['a'])
        self.assertEqual(actual_track.pop('album'), data['b'])
        self.assertEqual(actual_track.pop('title'), data['t'])
        self.assertEqual(len(actual_track), 0)

    def test_nowplay_expires(self):
        session_id, nowplay_url, _ = self.perform_handshake()
        data = {
            'a': 'Unknown Artist',
            'b': 'Unknown Album',
            't': 'Unknown Track',
            'l': '2',
            's': session_id
        }
        rep = post(nowplay_url, data=data)
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'OK')
        actual_track = self.get_current_track()
        self.assertIsNotNone(actual_track)
        self.assertEqual(actual_track.pop('artist'), data['a'])
        self.assertEqual(actual_track.pop('album'), data['b'])
        self.assertEqual(actual_track.pop('title'), data['t'])
        self.assertEqual(len(actual_track), 0)
        # Unfortunately it is necessary
        # because track should expire after 2 seconds
        sleep(2)
        self.assertIsNone(self.get_current_track())

    def test_nowplay_failed_without_session_id(self):
        rep = post(self.SUBMISSIONS_NOWPLAY_URL, data={})
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'BADSESSION')
        self.assertIsNone(self.get_current_track())

    def test_nowplay_failed_with_bad_session_id(self):
        _, nowplay_url, _ = self.perform_handshake()
        rep = post(nowplay_url, data={'s': 'invalid-session-id'})
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'BADSESSION')
        self.assertIsNone(self.get_current_track())

    def test_nowplay_failed_with_bad_data(self):
        session_id, nowplay_url, _ = self.perform_handshake()
        dataset = [
            {'b': 'Without', 't': 'Artist', 'l': '329'},
            {'a': 'Without', 't': 'Album', 'l': '329'},
            {'a': 'Without', 'b': 'Title', 'l': '329'},
            {'a': 'Without', 'b': 'Length', 't': 'Test'},
            {'a': 'With', 'b': 'Invalid', 't': 'Length', 'l': 'invalid'},
            {'a': 'With', 'b': 'Empty', 't': 'Length', 'l': ''},
            {'a': '', 'b': 'With Empty', 't': 'Artist', 'l': '329'},
            {'a': 'With Empty', 'b': '', 't': 'Album', 'l': '329'},
            {'a': 'With', 'b': 'Empty Title', 't': '', 'l': '329'},
            {}
        ]
        for data in dataset:
            rep = post(nowplay_url, data={**data, 's': session_id})
            self.assertEqual(rep.status_code, 200, rep.text)
            self.assertEqual(rep.text, 'OK')
            self.assertIsNone(self.get_current_track())
