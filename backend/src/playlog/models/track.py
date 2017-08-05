from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table

from playlog.models import metadata

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
