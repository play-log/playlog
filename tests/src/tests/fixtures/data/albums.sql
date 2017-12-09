INSERT INTO artist
    (id, name, first_play, last_play, plays)
VALUES
    (1, 'Decapitated', '2014-01-21T10:26:00', '2017-12-05T21:44:00', 958),
    (2, 'Amputated', '2012-12-05T17:01', '2012-12-05T17:22', 8)
;

INSERT INTO album
    (id, artist_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Anticult', '2017-07-06T15:08:00', '2017-12-05T18:34:00', 120),
    (2, 1, 'Blood Mantra', '2014-12-15T06:54:00', '2017-11-23T17:16:00', 144),
    (3, 1, 'Carnival Is Forever', '2014-02-08T09:50:00', '2017-11-23T22:50:00', 176),
    (4, 1, 'Nihility', '2014-02-09T00:22:00', '2017-12-05T21:22:00', 120),
    (5, 1, 'Organic Hallucinosis', '2014-01-24T15:08:00', '2017-12-05T15:38:00', 119),
    (6, 1, 'The Negation', '2014-01-21T10:26:00', '2017-12-05T21:44:00', 123),
    (7, 1, 'Winds Of Creation', '2014-02-09T13:37:00', '2017-12-04T12:29:00', 144),
    (8, 2, 'Wading Through Rancid Offal', '2012-12-05T17:01:00', '2012-12-05T17:22:00', 8)
;
