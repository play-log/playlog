from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata, utils

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
    return await utils.find_one(conn, album, kwargs)


async def update(conn, album_id):
    await utils.update(conn, album, album.c.id == album_id, {
        'plays': album.c.plays + 1,
        'last_play': datetime.utcnow()
    })


async def count_total(conn):
    return await conn.scalar(album.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(album.c.first_play >= since))
