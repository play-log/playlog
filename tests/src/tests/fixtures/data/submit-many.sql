INSERT INTO artist
    (name, first_play, last_play, plays)
VALUES
    ('Test', '2017-11-25T16:21', '2017-11-25T16:21', 1)
;

INSERT INTO album
    (artist_id, name, first_play, last_play, plays)
VALUES
    (1, 'Test', '2017-11-25T16:21', '2017-11-25T16:21', 1)
;

INSERT INTO track
    (album_id, name, first_play, last_play, plays)
VALUES
    (1, 'Test', '2017-11-25T16:21', '2017-11-25T16:21', 1)
;

INSERT INTO play
    (track_id, date)
VALUES
    (1, '2017-11-25T16:21')
;
