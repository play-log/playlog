from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func, select, true

from playlog.models import metadata, utils

track = Table(
    'track',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('album_id', ForeignKey('album.id', ondelete='CASCADE'), nullable=False),
    Column('name', String(500), nullable=False),
    Column('plays', Integer(), nullable=False),
    Column('first_play', DateTime(), nullable=False),
    Column('last_play', DateTime(), nullable=False),
    Column('is_favorite', Boolean(), nullable=False, default=False)
)


async def create(conn, album_id, name, is_favorite):
    now = datetime.utcnow()
    return await utils.create(conn, track, {
        'name': name,
        'album_id': album_id,
        'plays': 1,
        'first_play': now,
        'last_play': now,
        'is_favorite': is_favorite
    })


async def find_one(conn, **kwargs):
    return await utils.find_one(conn, track, kwargs)


async def update(conn, track_id, is_favorite):
    await utils.update(conn, track, track.c.id == track_id, {
        'plays': track.c.plays + 1,
        'last_play': datetime.utcnow(),
        'is_favorite': is_favorite
    })


async def count_total(conn):
    return await conn.scalar(track.count())


async def count_favorite(conn):
    return await conn.scalar(select([func.count()]).where(track.c.is_favorite == true()))


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(track.c.first_play >= since))
