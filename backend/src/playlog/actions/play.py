from sqlalchemy.sql import and_, func, select

from playlog.lib.validation import Int, ISODateTime, Length, OneOf, Optional, Period, validate
from playlog.models import album, artist, play, track


RECENT_LIMIT = 15


async def create(conn, track_id, date):
    await conn.execute(play.insert().values(track_id=track_id, date=date))


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
    result = await conn.scalar(select([play.c.date]).order_by(play.c.date.asc()).limit(1))
    return result.year if result else None


async def get_biggest_day(conn):
    day = func.date_trunc('DAY', play.c.date).label('day')
    plays = func.count().label('plays')
    result = await conn.execute(select([day, plays]).group_by(day).order_by(plays.desc()).limit(1))
    return await result.fetchone()


@validate(params={
    'period': Optional(Period()),
    'filter_kind': Optional(OneOf(['artist', 'album', 'track'])),
    'filter_value': Optional(Int())
})
async def count_for_period(conn, params):
    period = params.get('period')
    if not period:
        label_edge = 'year'
    else:
        label_edge = {
            'year': 'month',
            'month': 'day',
            'day': 'hour'
        }[period['kind']]
    label = func.date_trunc(label_edge, play.c.date).label('label')
    stmt = select([label, func.count().label('value')])
    if period:
        stmt = stmt.where(func.date_trunc(period['kind'], play.c.date) == period['value'])
    stmt = stmt.group_by(label).order_by(label)

    filter_kind = params.get('filter_kind')
    if filter_kind == 'artist':
        filter_column = artist.c.id
        from_clause = play.join(track).join(album).join(artist)
    elif filter_kind == 'album':
        filter_column = album.c.id
        from_clause = play.join(track).join(album)
    elif filter_kind == 'track':
        filter_column = track.c.id
        from_clause = play.join(track)
    else:
        filter_column = None
        from_clause = None
    if filter_column is not None:
        filter_value = params.get('filter_value')
        if not filter_value:
            raise ValueError(
                'Unable to filter by {}: '
                'value is not specified'.format(
                    filter_column
                )
            )
        stmt = stmt.where(filter_column == filter_value)
    if from_clause is not None:
        stmt = stmt.select_from(from_clause)

    result = await conn.execute(stmt)
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


@validate(
    params={
        'artist': Optional(Length(min_len=1, max_len=50)),
        'album': Optional(Length(min_len=1, max_len=50)),
        'track': Optional(Length(min_len=1, max_len=50)),
        'date_lt': Optional(ISODateTime()),
        'date_gt': Optional(ISODateTime()),
        'order_field': Optional(OneOf(['artist', 'album', 'track', 'date'])),
        'order_direction': Optional(OneOf(['asc', 'desc'])),
        'limit': Int(min_val=1, max_val=100),
        'offset': Int(min_val=0)
    }
)
async def find_many(conn, params):
    artist_name = artist.c.name.label('artist')
    album_name = album.c.name.label('album')
    track_name = track.c.name.label('track')

    filters = []
    if 'artist' in params:
        filters.append(artist_name.ilike('%{}%'.format(params['artist'])))
    if 'album' in params:
        filters.append(album_name.ilike('%{}%'.format(params['album'])))
    if 'track' in params:
        filters.append(track_name.ilike('%{}%'.format(params['track'])))
    if 'date_gt' in params:
        filters.append(play.c.date >= params['date_gt'])
    if 'date_lt' in params:
        filters.append(play.c.date <= params['date_lt'])

    order_field = params.get('order_field', 'date')
    if order_field == 'artist':
        order_clause = artist_name
    elif order_field == 'album':
        order_clause = album_name
    elif order_field == 'track':
        order_clause = track_name
    else:
        order_clause = play.c[order_field]
    order_direction = params.get('order_direction', 'desc')
    order_clause = getattr(order_clause, order_direction)()

    stmt = select([
        artist_name,
        album_name,
        track_name,
        artist.c.id.label('artist_id'),
        album.c.id.label('album_id'),
        play.c.track_id.label('track_id'),
        play.c.date.label('date')
    ])

    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.select_from(play.join(track).join(album).join(artist))
    total = await conn.scalar(stmt.with_only_columns([func.count(play.c.track_id)]))
    stmt = stmt.offset(params['offset']).limit(params['limit']).order_by(order_clause)
    result = await conn.execute(stmt)
    items = await result.fetchall()

    return {'items': items, 'total': total}


async def find_for_track(conn, track_id):
    query = select([play]).where(play.c.track_id == track_id).order_by(play.c.date.asc())
    result = await conn.execute(query)
    return await result.fetchall()
