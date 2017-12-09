INSERT INTO artist
    (id, name, first_play, last_play, plays)
VALUES
    (1, 'Decapitated', '2014-01-21T10:26:00', '2017-12-05T21:44:00', 958)
;

INSERT INTO album
    (id, artist_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Winds Of Creation', '2014-02-09T13:37:00', '2017-12-04T12:29:00', 144)
;

INSERT INTO track
    (id, album_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Winds Of Creation', '2014-08-22T18:07:00', '2017-12-04T11:46:00', 16),
    (2, 1, 'Way To Salvation May', '2014-05-27T16:52:00', '2017-12-04T12:01:00', 16),
    (3, 1, 'Dance Macabre', '2014-12-16T10:16:00', '2017-12-04T12:25:00', 16),
    (4, 1, 'Mandatory Suicide', '2014-02-09T13:37:00', '2017-12-04T12:29:00', 16),
    (5, 1, 'Humans Dust', '2014-08-22T18:53:00', '2017-12-04T12:21:00', 16),
    (6, 1, 'Blessed', '2014-08-22T18:33:00', '2017-12-04T11:51:00', 16),
    (7, 1, 'Nine Steps', '2014-08-22T18:59:00', '2017-12-04T12:22:00', 16),
    (8, 1, 'The First Damned', '2014-08-22T18:39:00', '2017-12-04T11:57:00', 16),
    (9, 1, 'The Eye Of Horus', '2014-02-28T13:49:00', '2017-12-04T12:06:00', 16)
;
