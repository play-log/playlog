from datetime import datetime, timedelta

from requests import post

from tests.submissions import TestCase


class TestSubmissionSubmit(TestCase):
    def test_submit_one_success(self):
        session_id, _, submit_url = self.perform_handshake()
        date = datetime(2017, 11, 25, 14, 58)
        rep = post(submit_url, data={
            'a[0]': 'Fleshgod Apocalypse',
            'b[0]': 'Labyrinth',
            't[0]': 'Prologue',
            'i[0]': str(int(date.timestamp())),
            's': session_id
        })
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'OK')

        artists = self.get_artists()
        self.assertEqual(len(artists), 1)
        artist = dict(artists[0])
        self.assertEqual(artist, {
            'id': 1,
            'name': 'Fleshgod Apocalypse',
            'plays': 1,
            'first_play': date,
            'last_play': date
        })

        albums = self.get_albums()
        self.assertEqual(len(albums), 1)
        album = dict(albums[0])
        self.assertEqual(album, {
            'id': 1,
            'artist_id': 1,
            'name': 'Labyrinth',
            'plays': 1,
            'first_play': date,
            'last_play': date
        })

        tracks = self.get_tracks()
        self.assertEqual(len(tracks), 1)
        track = dict(tracks[0])
        self.assertEqual(track, {
            'id': 1,
            'album_id': 1,
            'name': 'Prologue',
            'plays': 1,
            'first_play': date,
            'last_play': date
        })

        plays = self.get_plays()
        self.assertEqual(len(plays), 1)
        play = dict(plays[0])
        self.assertEqual(play, {
            'track_id': 1,
            'date': date
        })

    def test_submit_many_success(self):
        date = datetime(2017, 11, 25, 16, 21)
        session_id, _, submit_url = self.perform_handshake()
        rep = post(submit_url, data={
            # Submit existing track
            'a[0]': 'Test',
            'b[0]': 'Test',
            't[0]': 'Test',
            'i[0]': str(int((date + timedelta(minutes=10)).timestamp())),
            # Submit new track for existing album and artist
            'a[1]': 'Test',
            'b[1]': 'Test',
            't[1]': 'Test new track',
            'i[1]': str(int((date + timedelta(minutes=20)).timestamp())),
            # Submit new album and track for existing artist
            'a[2]': 'Test',
            'b[2]': 'Test new album',
            't[2]': 'Test new track',
            'i[2]': str(int((date + timedelta(minutes=30)).timestamp())),
            # Submit new artist
            'a[3]': 'Test new artist',
            'b[3]': 'Test',
            't[3]': 'Test',
            'i[3]': str(int((date + timedelta(minutes=40)).timestamp())),
            # Session
            's': session_id
        })
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'OK')

        artists = self.get_artists()
        self.assertEqual(len(artists), 2)
        artist1 = dict(artists[0])
        self.assertEqual(artist1, {
            'id': 1,
            'name': 'Test',
            'plays': 4,
            'first_play': date,
            'last_play': date + timedelta(minutes=30)
        })
        artist2 = dict(artists[1])
        self.assertEqual(artist2, {
            'id': 2,
            'name': 'Test new artist',
            'plays': 1,
            'first_play': date + timedelta(minutes=40),
            'last_play': date + timedelta(minutes=40),
        })

        albums = self.get_albums()
        self.assertEqual(len(albums), 3)
        album1 = dict(albums[0])
        self.assertEqual(album1, {
            'id': 1,
            'artist_id': 1,
            'name': 'Test',
            'plays': 3,
            'first_play': date,
            'last_play': date + timedelta(minutes=20)
        })
        album2 = dict(albums[1])
        self.assertEqual(album2, {
            'id': 2,
            'artist_id': 1,
            'name': 'Test new album',
            'plays': 1,
            'first_play': date + timedelta(minutes=30),
            'last_play': date + timedelta(minutes=30)
        })
        album3 = dict(albums[2])
        self.assertEqual(album3, {
            'id': 3,
            'artist_id': 2,
            'name': 'Test',
            'plays': 1,
            'first_play': date + timedelta(minutes=40),
            'last_play': date + timedelta(minutes=40)
        })

        tracks = self.get_tracks()
        self.assertEqual(len(tracks), 4)
        track1 = dict(tracks[0])
        self.assertEqual(track1, {
            'id': 1,
            'album_id': 1,
            'name': 'Test',
            'plays': 2,
            'first_play': date,
            'last_play': date + timedelta(minutes=10)
        })
        track2 = dict(tracks[1])
        self.assertEqual(track2, {
            'id': 2,
            'album_id': 1,
            'name': 'Test new track',
            'plays': 1,
            'first_play': date + timedelta(minutes=20),
            'last_play': date + timedelta(minutes=20)
        })
        track3 = dict(tracks[2])
        self.assertEqual(track3, {
            'id': 3,
            'album_id': 2,
            'name': 'Test new track',
            'plays': 1,
            'first_play': date + timedelta(minutes=30),
            'last_play': date + timedelta(minutes=30)
        })
        track4 = dict(tracks[3])
        self.assertEqual(track4, {
            'id': 4,
            'album_id': 3,
            'name': 'Test',
            'plays': 1,
            'first_play': date + timedelta(minutes=40),
            'last_play': date + timedelta(minutes=40)
        })

    def test_submit_many_exceeded(self):
        keys = ['a', 'b', 't']
        data = {}
        for i in range(100):
            value = 'Test {}'.format(i)
            for k in keys:
                data['{}[{}]'.format(k, i)] = value
            data['i[{}]'.format(i)] = i

        session_id, _, submit_url = self.perform_handshake()
        data['s'] = session_id
        rep = post(submit_url, data=data)
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'OK')
        self.assertEqual(self.count_artists(), 50)
        self.assertEqual(self.count_albums(), 50)
        self.assertEqual(self.count_tracks(), 50)
        self.assertEqual(self.count_plays(), 50)

    def test_submit_failed_without_session_id(self):
        rep = post(self.SUBMISSIONS_SUBMIT_URL, data={})
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'BADSESSION')

    def test_submit_failed_with_bad_session_id(self):
        session_id, _, submit_url = self.perform_handshake()
        rep = post(submit_url, data={'s': 'invalid-session-id'})
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'BADSESSION')

    def test_submit_failed_with_invalid_data(self):
        session_id, _, submit_url = self.perform_handshake()
        dataset = [
            {},
            {'a[0]': 'Without', 'b[0]': 'Title', 'i[0]': '0'},
            {'a[0]': 'Without', 't[0]': 'Album', 'i[0]': '0'},
            {'b[0]': 'Without', 't[0]': 'Artist', 'i[0]': '0'},
            {'a[0]': 'Without', 'b[0]': 'Timestamp', 't[0]': 'Test'},
            {'a[0]': '', 'b[0]': 'With Empty', 't[0]': 'Artist', 'i[0]': '0'},
            {'a[0]': 'With Empty', 'b[0]': '', 't[0]': 'Album', 'i[0]': '0'},
            {'a[0]': 'With Empty', 'b[0]': 'Track', 't[0]': '', 'i[0]': '0'},
            {'a[0]': 'With', 'b[0]': 'Empty', 't[0]': 'Timestamp', 'i[0]': ''},
            {'a[0]': 'With', 'b[0]': 'Invalid', 't[0]': 'Timestamp', 'i[0]': 'xxx'}
        ]
        for data in dataset:
            rep = post(submit_url, data={**data, 's': session_id})
            self.assertEqual(rep.status_code, 200, rep.text)
            self.assertEqual(rep.text, 'OK')
            self.assertEqual(self.count_artists(), 0)
            self.assertEqual(self.count_albums(), 0)
            self.assertEqual(self.count_tracks(), 0)
            self.assertEqual(self.count_plays(), 0)

    def test_submit_existing_date_failed(self):
        date = datetime(2017, 11, 25, 15, 55)
        session_id, _, submit_url = self.perform_handshake()
        rep = post(submit_url, data={
            'a[0]': 'Test',
            'b[0]': 'Test',
            't[0]': 'Test',
            'i[0]': str(int(date.timestamp())),
            's': session_id
        })
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(rep.text, 'OK')

        for key in ('artists', 'albums', 'tracks'):
            items = getattr(self, 'get_{}'.format(key))()
            self.assertEqual(len(items), 1)
            item = dict(items[0])
            self.assertEqual(item['plays'], 1)
            self.assertEqual(item['first_play'], date)
            self.assertEqual(item['last_play'], date)
        plays = self.get_plays()
        self.assertEqual(len(plays), 1)
        play = dict(plays[0])
        self.assertEqual(play['track_id'], 1)
        self.assertEqual(play['date'], date)
