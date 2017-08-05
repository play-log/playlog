from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table

from playlog.models import metadata

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


async def count_total(conn):
    return await conn.scalar(album.count())
