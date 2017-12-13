from schematics.types import IntType, StringType, UTCDateTimeType
from sqlalchemy.sql import and_, func, select

from playlog.lib.validation import OrderType, validate
from playlog.models import album, artist, track


async def create(conn, album_id, name, plays, first_play, last_play):
    return await conn.scalar(track.insert().values(
        name=name,
        album_id=album_id,
        plays=plays,
        first_play=first_play,
        last_play=last_play
    ))


async def find_one(conn, **kwargs):
    query = select([
        artist.c.id.label('artist_id'),
        artist.c.name.label('artist_name'),
        album.c.name.label('album_name'),
        track
    ])
    for key, value in kwargs.items():
        query = query.where(getattr(track.c, key) == value)
    query = query.select_from(track.join(album).join(artist))
    result = await conn.execute(query)
    return await result.fetchone()


@validate.params(
    artist=StringType(min_length=1, max_length=50),
    album=StringType(min_length=1, max_length=50),
    track=StringType(min_length=1, max_length=50),
    first_play_lt=UTCDateTimeType(),
    first_play_gt=UTCDateTimeType(),
    last_play_lt=UTCDateTimeType(),
    last_play_gt=UTCDateTimeType(),
    order=OrderType('artist', 'album', 'track', 'first_play', 'last_play', 'plays'),
    limit=IntType(required=True, min_value=1, max_value=100),
    offset=IntType(required=True, min_value=0)
)
async def find_many(conn, params):
    artist_name = artist.c.name.label('artist')
    album_name = album.c.name.label('album')

    filters = []
    if 'artist' in params:
        filters.append(artist_name.ilike('%{}%'.format(params['artist'])))
    if 'album' in params:
        filters.append(album_name.ilike('%{}%'.format(params['album'])))
    if 'track' in params:
        filters.append(track.c.name.ilike('%{}%'.format(params['track'])))
    if 'first_play_gt' in params:
        filters.append(track.c.first_play >= params['first_play_gt'])
    if 'first_play_lt' in params:
        filters.append(track.c.first_play <= params['first_play_lt'])
    if 'last_play_gt' in params:
        filters.append(track.c.last_play >= params['last_play_gt'])
    if 'last_play_lt' in params:
        filters.append(track.c.last_play <= params['last_play_lt'])

    order = params.get('order')
    order_field = order['column'] if order else 'artist'
    order_direction = order['direction'] if order else 'asc'
    if order_field == 'artist':
        order_clause = artist_name
    elif order_field == 'album':
        order_clause = album_name
    elif order_field == 'track':
        order_clause = track.c.name
    else:
        order_clause = track.c[order_field]
    order_clause = getattr(order_clause, order_direction)()

    stmt = select([artist.c.id.label('artist_id'), artist_name, album_name, track])
    if filters:
        stmt = stmt.where(and_(*filters))
    stmt = stmt.select_from(track.join(album).join(artist))
    total = await conn.scalar(stmt.with_only_columns([func.count(track.c.id)]))
    stmt = stmt.offset(params['offset']).limit(params['limit']).order_by(order_clause)
    result = await conn.execute(stmt)
    items = await result.fetchall()
    return {'items': items, 'total': total}


async def find_for_album(conn, album_id):
    query = select([track]).where(track.c.album_id == album_id).order_by(track.c.plays.desc())
    result = await conn.execute(query)
    return await result.fetchall()


async def update(conn, track_id, **params):
    await conn.execute(track.update().values(**params).where(track.c.id == track_id))


async def count_total(conn):
    return await conn.scalar(track.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(track.c.first_play >= since))


async def submit(conn, album_id, name, date):
    data = await find_one(conn, album_id=album_id, name=name)
    if data:
        track_id = data['id']
        await update(
            conn=conn,
            track_id=track_id,
            plays=track.c.plays + 1,
            last_play=date
        )
    else:
        track_id = await create(
            conn=conn,
            album_id=album_id,
            name=name,
            plays=1,
            first_play=date,
            last_play=date
        )
    return track_id
