from schematics.types import IntType, StringType, UTCDateTimeType
from sqlalchemy.sql import and_, func, select

from playlog.lib.validation import OrderType, validate
from playlog.models import artist


async def create(conn, name, plays, first_play, last_play):
    return await conn.scalar(artist.insert().values(
        name=name,
        plays=plays,
        first_play=first_play,
        last_play=last_play
    ))


async def find_one(conn, **kwargs):
    query = select([artist])
    for key, value in kwargs.items():
        query = query.where(getattr(artist.c, key) == value)
    result = await conn.execute(query)
    return await result.fetchone()


@validate.params(
    name=StringType(min_length=1, max_length=50),
    first_play_lt=UTCDateTimeType(),
    first_play_gt=UTCDateTimeType(),
    last_play_lt=UTCDateTimeType(),
    last_play_gt=UTCDateTimeType(),
    order=OrderType('name', 'first_play', 'last_play', 'plays'),
    limit=IntType(required=True, min_value=1, max_value=100),
    offset=IntType(required=True, min_value=0)
)
async def find_many(conn, params):
    filters = []
    if 'name' in params:
        filters.append(artist.c.name.ilike('%{}%'.format(params['name'])))
    if 'first_play_gt' in params:
        filters.append(artist.c.first_play >= params['first_play_gt'])
    if 'first_play_lt' in params:
        filters.append(artist.c.first_play <= params['first_play_lt'])
    if 'last_play_gt' in params:
        filters.append(artist.c.last_play >= params['last_play_gt'])
    if 'last_play_lt' in params:
        filters.append(artist.c.last_play <= params['last_play_lt'])

    order = params.get('order')
    if order:
        order_clause = getattr(artist.c[order['column']], order.get('direction', 'asc'))()
    else:
        order_clause = artist.c.name.asc()

    stmt = select([artist])
    if filters:
        stmt = stmt.where(and_(*filters))
    total = await conn.scalar(stmt.with_only_columns([func.count(artist.c.id)]))
    stmt = stmt.offset(params['offset']).limit(params['limit']).order_by(order_clause)
    result = await conn.execute(stmt)
    items = await result.fetchall()

    return {'items': items, 'total': total}


async def update(conn, artist_id, **params):
    await conn.execute(artist.update().values(**params).where(artist.c.id == artist_id))


async def count_total(conn):
    return await conn.scalar(artist.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(artist.c.first_play >= since))


async def submit(conn, name, date):
    data = await find_one(conn, name=name)
    if data:
        artist_id = data['id']
        await update(
            conn=conn,
            artist_id=artist_id,
            plays=artist.c.plays + 1,
            last_play=date
        )
    else:
        artist_id = await create(
            conn=conn,
            name=name,
            plays=1,
            first_play=date,
            last_play=date
        )
    return artist_id
