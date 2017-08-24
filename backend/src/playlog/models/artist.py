from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata, utils


ORDER_DIRECTIONS = ['asc', 'desc']
DEFAULT_ORDER_DIRECTION = 'asc'
ORDER_FIELDS = ['name', 'first_play', 'last_play', 'plays']
DEFAULT_ORDER_FIELD = 'name'


artist = Table(
    'artist',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(500), nullable=False),
    Column('plays', Integer(), nullable=False),
    Column('first_play', DateTime(), nullable=False),
    Column('last_play', DateTime(), nullable=False)
)


async def create(conn, name):
    now = datetime.utcnow()
    return await utils.create(conn, artist, {
        'name': name,
        'plays': 1,
        'first_play': now,
        'last_play': now
    })


async def find_one(conn, **kwargs):
    return await utils.find_one(conn, artist, kwargs)


async def find_many(conn, offset, limit, **kwargs):
    order_field = kwargs.get('order_field', DEFAULT_ORDER_FIELD)
    order_expr = getattr(artist.c, order_field)
    order_direction = kwargs.get('order_direction', DEFAULT_ORDER_DIRECTION)
    order_expr = getattr(order_expr, order_direction)

    name = kwargs.get('name')
    first_play_lt = kwargs.get('first_play_lt')
    first_play_gt = kwargs.get('first_play_gt')
    last_play_lt = kwargs.get('last_play_lt')
    last_play_gt = kwargs.get('last_play_gt')

    query = select([artist])
    if name:
        query = query.where(artist.c.name.ilike('%{}%'.format(name)))
    if first_play_gt:
        query = query.where(artist.c.first_play >= first_play_gt)
    if first_play_lt:
        query = query.where(artist.c.first_play <= first_play_lt)
    if last_play_gt:
        query = query.where(artist.c.last_play >= last_play_gt)
    if last_play_lt:
        query = query.where(artist.c.last_play <= last_play_lt)
    total = await conn.scalar(query.with_only_columns([func.count(artist.c.id)]))
    query = query.offset(offset).limit(limit).order_by(order_expr())
    result = await conn.execute(query)
    items = await result.fetchall()

    return {'items': items, 'total': total}


async def update(conn, artist_id):
    await utils.update(conn, artist, artist.c.id == artist_id, {
        'plays': artist.c.plays + 1,
        'last_play': datetime.utcnow()
    })


async def count_total(conn):
    return await conn.scalar(artist.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(artist.c.first_play >= since))
