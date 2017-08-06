from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata

artist = Table(
    'artist',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(500), nullable=False),
    Column('plays', Integer(), nullable=False),
    Column('first_play', DateTime(), nullable=False),
    Column('last_play', DateTime(), nullable=False)
)


async def count_total(conn):
    return await conn.scalar(artist.count())


async def count_new(conn, since):
    return await conn.scalar(select([func.count()]).where(artist.c.first_play >= since))
