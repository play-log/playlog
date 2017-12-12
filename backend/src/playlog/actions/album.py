from schematics.types import IntType, StringType, UTCDateTimeType
from sqlalchemy.sql import and_, func, select

from playlog.lib.validation import validate
from playlog.models import album, artist


async def create(conn, artist_id, name, plays, first_play, last_play):
    return await conn.scalar(album.insert().values(
        artist_id=artist_id,
        name=name,
        plays=plays,
        first_play=first_play,
        last_play=last_play
    ))


async def find_one(conn, **kwargs):
    query = select([artist.c.name.label('artist_name'), album])
    for key, value in kwargs.items():
        query = query.where(getattr(album.c, key) == value)
    query = query.select_from(album.join(artist))
    result = await conn.execute(query)
    return await result.fetchone()


@validate.params(
    artist=StringType(min_length=1, max_length=50),
    name=StringType(min_length=1, max_length=50),
    first_play_lt=UTCDateTimeType(),
    first_play_gt=UTCDateTimeType(),
    last_play_lt=UTCDateTimeType(),
    last_play_gt=UTCDateTimeType(),
    order_field=StringType(choices=['artist', 'name', 'first_play', 'last_play', 'plays']),
    order_direction=StringType(choices=['asc', 'desc']),
    limit=IntType(required=True, min_value=1, max_value=100),
    offset=IntType(required=True, min_value=0)
)
async def find_many(conn, params):
    artist_name = artist.c.name.label('artist')

    filters = []
    if 'artist' in params:
        filters.append(artist_name.ilike('%{}%'.format(params['artist'])))
    if 'name' in params:
        filters.append(album.c.name.ilike('%{}%'.format(params['name'])))
    if 'first_play_gt' in params:
        filters.append(album.c.first_play >= params['first_play_gt'])
    if 'first_play_lt' in params:
        filters.append(album.c.first_play <= params['first_play_lt'])
    if 'last_play_gt' in params:
        filters.append(album.c.last_play >= params['last_play_gt'])
    if 'last_play_lt' in params:
        filters.append(album.c.last_play <= params['last_play_lt'])

    order_field = params.get('order_field', 'artist')
    if order_field == 'artist':
        order_clause = artist_name
    else:
        order_clause = album.c[order_field]
    order_direction = params.get('order_direction', 'asc')
    order_clause = getattr(order_clause, order_direction)()

    stmt = select([album, artist_name]).select_from(album.join(artist))

    if filters:
        stmt = stmt.where(and_(*filters))

    total = await conn.scalar(stmt.with_only_columns([func.count(album.c.id)]))

    stmt = stmt.offset(params['offset']).limit(params['limit']).order_by(order_clause)

    result = await conn.execute(stmt)
    items = await result.fetchall()

    return {'items': items, 'total': total}


async def find_for_artist(conn, artist_id):
    query = select([album]).where(album.c.artist_id == artist_id).order_by(album.c.plays.desc())
    result = await conn.execute(query)
    return await result.fetchall()


async def update(conn, album_id, **params):
    await conn.execute(album.update().values(**params).where(album.c.id == album_id))


async def count_total(conn):
    return await conn.scalar(album.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(album.c.first_play >= since))


async def submit(conn, artist_id, name, date):
    data = await find_one(conn, artist_id=artist_id, name=name)
    if data:
        album_id = data['id']
        await update(
            conn=conn,
            album_id=album_id,
            plays=album.c.plays + 1,
            last_play=date
        )
    else:
        album_id = await create(
            conn=conn,
            artist_id=artist_id,
            name=name,
            plays=1,
            first_play=date,
            last_play=date
        )
    return album_id
