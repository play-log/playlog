from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

artist = Table(
    'artist',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(500), nullable=False),
    Column('plays', Integer(), nullable=False),
    Column('first_play', DateTime(), nullable=False),
    Column('last_play', DateTime(), nullable=False)
)

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

play = Table(
    'play',
    metadata,
    Column('track_id', ForeignKey('track.id', ondelete='CASCADE'), primary_key=True),
    Column('date', DateTime(), primary_key=True)
)
