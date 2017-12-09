INSERT INTO artist
    (id, name, first_play, last_play, plays)
VALUES
    (1, 'Ulcerate', '2013-05-19T16:24:00', '2017-08-31T23:04:00', 2351)
;

INSERT INTO album
    (id, artist_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Shrines Of Paralysis', '2016-10-24T10:32:00', '2017-08-31T15:16:00', 442)
;

INSERT INTO track
    (id, album_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Extinguished Light', '2016-10-24T11:23:00', '2017-08-31T15:07:00', 70)
;

INSERT INTO play
    (track_id, date)
VALUES
    (1, '2016-10-24T11:23:00'),
    (1, '2017-08-31T15:07:00')
;
