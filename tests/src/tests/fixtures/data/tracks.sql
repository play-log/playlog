INSERT INTO artist
    (id, name, first_play, last_play, plays)
VALUES
    (1, 'Ulcerate', '2013-05-19T16:24:00', '2017-08-31T23:04:00', 2351),
    (2, 'Sterbend', '2012-12-08T14:23:00', '2012-12-08T14:23:00', 1)
;

INSERT INTO album
    (id, artist_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Shrines Of Paralysis', '2016-10-24T10:32:00', '2017-08-31T15:16:00', 442),
    (2, 2, 'Einsamkeit', '2012-12-08T14:23:00', '2012-12-08T14:23:00', 1)
;

INSERT INTO track
    (id, album_id, name, first_play, last_play, plays)
VALUES
    (1, 1, 'Abrogation', '2016-10-24T10:32:00', '2017-08-31T14:09:00', 71),
    (2, 1, 'Extinguished Light', '2016-10-24T11:23:00', '2017-08-31T15:07:00', 70),
    (3, 1, 'Bow To Spite', '2016-10-24T11:13:00', '2017-08-31T14:51:00', 67),
    (4, 1, 'Yield To Naught', '2016-10-24T10:37:00', '2017-08-31T14:17:00', 65),
    (5, 1, 'Chasm Of Fire', '2016-10-24T11:15:00', '2017-08-31T14:59:00', 64),
    (6, 1, 'There Are No Saviours', '2016-10-24T10:45:00', '2017-08-31T14:25:00', 58),
    (7, 1, 'Shrines Of Paralysis', '2016-10-24T10:53:00', '2017-08-31T14:34:00', 55),
    (8, 1, 'End The Hope', '2016-10-24T11:32:00', '2017-08-31T15:16:00', 53),
    (9, 2, 'Introduction', '2012-12-08T14:23:00', '2012-12-08T14:23:00', 1)
;
