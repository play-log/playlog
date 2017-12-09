INSERT INTO artist
    (id, name, first_play, last_play, plays)
VALUES
    (1, 'Artist', '2017-12-03T20:30', '2017-12-03T20:30', 1)
;

INSERT INTO album
    (id, artist_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Album', '2017-12-03T20:30', '2017-12-03T20:30', 1)
;

INSERT INTO track
    (id, album_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Track', '2017-12-03T20:30', '2017-12-03T20:30', 1)
;

INSERT INTO play
    (track_id, date)
VALUES
    (1, '2017-12-03T20:30')
;
