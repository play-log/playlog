from sqlalchemy import Column, DateTime, ForeignKey, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata, utils
from playlog.models.artist import artist
from playlog.models.album import album
from playlog.models.track import track


ORDER_DIRECTIONS = ['asc', 'desc']
DEFAULT_ORDER_DIRECTION = 'desc'
ORDER_FIELDS = ['artist_name', 'album_name', 'track_name', 'date']
DEFAULT_ORDER_FIELD = 'date'

RECENT_LIMIT = 15


play = Table(
    'play',
    metadata,
    Column('track_id', ForeignKey('track.id', ondelete='CASCADE'), primary_key=True),
    Column('date', DateTime(), primary_key=True)
)


async def create(conn, track_id, date):
    await utils.create(conn, play, {
        'track_id': track_id,
        'date': date
    }, scalar=False)


async def is_date_exists(conn, date):
    return await conn.scalar(select([func.count()]).where(play.c.date == date)) > 0


async def count_total(conn):
    return await conn.scalar(play.count())


async def get_recent(conn):
    result = await conn.execute(
        select([
            artist.c.name.label('artist'),
            artist.c.id.label('artist_id'),
            album.c.name.label('album'),
            album.c.id.label('album_id'),
            track.c.name.label('track'),
            play.c.track_id.label('track_id'),
            play.c.date.label('date')
        ])
        .order_by(play.c.date.desc())
        .limit(RECENT_LIMIT)
        .select_from(play.join(track).join(album).join(artist))
    )
    return await result.fetchall()


async def get_listening_since(conn):
    return await conn.scalar(select([play.c.date]).order_by(play.c.date.asc()).limit(1))


async def get_biggest_day(conn):
    day = func.date_trunc('DAY', play.c.date).label('day')
    plays = func.count().label('plays')
    result = await conn.execute(select([day, plays]).group_by(day).order_by(plays.desc()).limit(1))
    return await result.fetchone()


async def count_per_year(conn):
    year = func.date_part('YEAR', play.c.date).label('year')
    plays = func.count().label('plays')
    result = await conn.execute(select([year, plays]).group_by(year).order_by(year))
    return await result.fetchall()


async def count_per_year_for_artist(conn, artist_id):
    year = func.date_part('YEAR', play.c.date).label('year')
    plays = func.count().label('plays')
    query = (select([year, plays]).where(artist.c.id == artist_id)
                                  .group_by(year)
                                  .order_by(year)
                                  .select_from(
                                      play.join(track)
                                          .join(album)
                                          .join(artist)))
    result = await conn.execute(query)
    return await result.fetchall()


async def count_per_year_for_album(conn, album_id):
    year = func.date_part('YEAR', play.c.date).label('year')
    plays = func.count().label('plays')
    query = (select([year, plays]).where(album.c.id == album_id)
                                  .group_by(year)
                                  .order_by(year)
                                  .select_from(
                                      play.join(track)
                                          .join(album)))
    result = await conn.execute(query)
    return await result.fetchall()


async def count_per_year_for_track(conn, track_id):
    year = func.date_part('YEAR', play.c.date).label('year')
    plays = func.count().label('plays')
    query = (select([year, plays]).where(play.c.track_id == track_id)
                                  .group_by(year)
                                  .order_by(year))
    result = await conn.execute(query)
    return await result.fetchall()


async def get_longest_streak(conn):
    result = await conn.execute("""
        WITH RECURSIVE days AS (
            SELECT date_trunc('day', date) AS day FROM play GROUP BY day
        ), pairs AS (
            SELECT
                day AS end_date,
                lag(day) OVER (ORDER BY day) AS start_date
            FROM days
        ), intervals AS (
            SELECT start_date, end_date FROM pairs
            WHERE (end_date - start_date) = '1 day'::interval
        ), streaks AS (
            SELECT start_date, end_date, 1 as days FROM intervals
            UNION
            SELECT a.start_date, b.end_date, b.days + 1 as days FROM intervals a
            JOIN streaks b ON a.end_date = b.start_date
        ), longest_streak AS (
            SELECT * FROM streaks ORDER BY days DESC LIMIT 1
        ) SELECT *, (
            SELECT COUNT(*) FROM play
            WHERE date >= longest_streak.start_date
            AND date < longest_streak.end_date + '1 day'::interval
        ) as plays FROM longest_streak;
    """)
    return await result.fetchone()


async def get_current_streak(conn):
    result = await conn.execute("""
        WITH RECURSIVE days AS (
            SELECT date_trunc('day', date) AS day FROM play GROUP BY day ORDER BY day DESC
        ), pairs AS (
            SELECT
                day AS end_date,
                lag(day) OVER (ORDER BY day) AS start_date
            FROM days
        ), r AS (
            SELECT
                date_trunc('day', now() at time zone 'utc') AS start_date,
                date_trunc('day', now() at time zone 'utc') AS end_date
            UNION
            SELECT b.start_date, b.end_date FROM r a JOIN pairs b ON b.end_date = a.start_date
            WHERE b.end_date - b.start_date <= '1 day'::interval
        ), current_interval AS (
            SELECT min(start_date) as start_date, max(end_date) as end_date FROM r
        ) SELECT
            start_date,
            end_date,
            (extract(epoch from (end_date - start_date)) / 86400) as days,
            (
                SELECT COUNT(*) FROM play
                WHERE date >= start_date
                AND date < end_date + '1 day'::interval
            ) as plays
        FROM current_interval;
    """)
    return await result.fetchone()


async def find_many(conn, offset, limit, **kwargs):
    artist_name = artist.c.name.label('artist')
    album_name = album.c.name.label('album')
    track_name = track.c.name.label('track')

    order_field = kwargs.get('order_field', DEFAULT_ORDER_FIELD)
    if order_field == 'artist_name':
        order_expr = artist_name
    elif order_field == 'album_name':
        order_expr = album_name
    elif order_field == 'track_name':
        order_expr = track_name
    else:
        order_expr = getattr(play.c, order_field)
    order_direction = kwargs.get('order_direction', DEFAULT_ORDER_DIRECTION)
    order_expr = getattr(order_expr, order_direction)

    query = select([
        artist_name,
        album_name,
        track_name,
        artist.c.id.label('artist_id'),
        album.c.id.label('album_id'),
        play.c.track_id.label('track_id'),
        play.c.date.label('date')
    ])

    if 'artist_name' in kwargs:
        query = query.where(artist_name.ilike('%{}%'.format(kwargs['artist_name'])))
    if 'album_name' in kwargs:
        query = query.where(album_name.ilike('%{}%'.format(kwargs['album_name'])))
    if 'track_name' in kwargs:
        query = query.where(track_name.ilike('%{}%'.format(kwargs['track_name'])))
    if 'date_gt' in kwargs:
        query = query.where(play.c.date >= kwargs['date_gt'])
    if 'date_lt' in kwargs:
        query = query.where(play.c.date <= kwargs['date_lt'])

    from_clause = play.join(track).join(album).join(artist)

    total = await conn.scalar(
        query.select_from(from_clause)
             .with_only_columns([func.count(play.c.track_id)])
    )

    query = query.offset(offset).limit(limit).order_by(order_expr())
    query = query.select_from(from_clause)

    result = await conn.execute(query)
    items = await result.fetchall()

    return {'items': items, 'total': total}


async def find_for_track(conn, track_id):
    query = select([play]).where(play.c.track_id == track_id).order_by(play.c.date.asc())
    result = await conn.execute(query)
    return await result.fetchall()
