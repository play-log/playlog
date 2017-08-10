from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata, utils

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


async def update(conn, artist_id):
    await utils.update(conn, artist, artist.c.id == artist_id, {
        'plays': artist.c.plays + 1,
        'last_play': datetime.utcnow()
    })


async def count_total(conn):
    return await conn.scalar(artist.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(artist.c.first_play >= since))
