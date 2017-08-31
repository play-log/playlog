from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata, utils
from playlog.models.artist import artist


ORDER_DIRECTIONS = ['asc', 'desc']
DEFAULT_ORDER_DIRECTION = 'asc'
ORDER_FIELDS = ['artist_name', 'album_name', 'first_play', 'last_play', 'plays']
DEFAULT_ORDER_FIELD = 'artist_name'


album = Table(
    'album',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('artist_id', ForeignKey('artist.id', ondelete='CASCADE'), nullable=False),
    Column('name', String(500), nullable=False),
    Column('plays', Integer(), nullable=False),
    Column('first_play', DateTime(), nullable=False),
    Column('last_play', DateTime(), nullable=False)
)


async def create(conn, artist_id, name):
    now = datetime.utcnow()
    return await utils.create(conn, album, {
        'name': name,
        'artist_id': artist_id,
        'plays': 1,
        'first_play': now,
        'last_play': now
    })


async def find_one(conn, **kwargs):
    query = select([artist.c.name.label('artist_name'), album])
    for key, value in kwargs.items():
        query = query.where(getattr(album.c, key) == value)
    query = query.select_from(album.join(artist))
    result = await conn.execute(query)
    return await result.fetchone()


async def find_many(conn, offset, limit, **kwargs):
    artist_name = artist.c.name.label('artist')

    order_field = kwargs.get('order_field', DEFAULT_ORDER_FIELD)
    if order_field == 'artist_name':
        order_expr = artist_name
    elif order_field == 'album_name':
        order_expr = album.c.name
    else:
        order_expr = getattr(album.c, order_field)
    order_direction = kwargs.get('order_direction', DEFAULT_ORDER_DIRECTION)
    order_expr = getattr(order_expr, order_direction)

    query = select([album, artist_name])

    if 'artist_name' in kwargs:
        query = query.where(artist_name.ilike('%{}%'.format(kwargs['artist_name'])))
    if 'album_name' in kwargs:
        query = query.where(album.c.name.ilike('%{}%'.format(kwargs['album_name'])))
    if 'first_play_gt' in kwargs:
        query = query.where(album.c.first_play >= kwargs['first_play_gt'])
    if 'first_play_lt' in kwargs:
        query = query.where(album.c.first_play <= kwargs['first_play_lt'])
    if 'last_play_gt' in kwargs:
        query = query.where(album.c.last_play >= kwargs['last_play_gt'])
    if 'last_play_lt' in kwargs:
        query = query.where(album.c.last_play <= kwargs['last_play_lt'])

    from_clause = album.join(artist)

    total = await conn.scalar(query.select_from(from_clause).with_only_columns([func.count(album.c.id)]))

    query = query.offset(offset).limit(limit).order_by(order_expr())
    query = query.select_from(from_clause)

    result = await conn.execute(query)
    items = await result.fetchall()

    return {'items': items, 'total': total}


async def find_for_artist(conn, artist_id):
    query = select([album]).where(album.c.artist_id == artist_id).order_by(album.c.plays.desc())
    result = await conn.execute(query)
    return await result.fetchall()


async def update(conn, album_id):
    await utils.update(conn, album, album.c.id == album_id, {
        'plays': album.c.plays + 1,
        'last_play': datetime.utcnow()
    })


async def count_total(conn):
    return await conn.scalar(album.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(album.c.first_play >= since))
