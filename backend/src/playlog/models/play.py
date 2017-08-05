from sqlalchemy import Column, DateTime, ForeignKey, Table

from playlog.models import metadata

play = Table(
    'play',
    metadata,
    Column('track_id', ForeignKey('track.id', ondelete='CASCADE'), primary_key=True),
    Column('date', DateTime(), primary_key=True)
)


async def count_total(conn):
    return await conn.scalar(play.count())
