from sqlalchemy import Column, DateTime, ForeignKey, Table
from sqlalchemy.sql import func, select

from playlog.models import metadata
from playlog.models.artist import artist
from playlog.models.album import album
from playlog.models.track import track


RECENT_LIMIT = 15


play = Table(
    'play',
    metadata,
    Column('track_id', ForeignKey('track.id', ondelete='CASCADE'), primary_key=True),
    Column('date', DateTime(), primary_key=True)
)


async def count_total(conn):
    return await conn.scalar(play.count())


async def get_recent(conn):
    result = await conn.execute(
        select([
            artist.c.name.label('artist'),
            album.c.name.label('album'),
            track.c.name.label('track'),
            track.c.is_favorite.label('is_favorite'),
            play.c.date.label('date')
        ])
        .order_by(play.c.date.desc())
        .limit(RECENT_LIMIT)
        .select_from(play.join(track).join(album).join(artist))
    )
    return await result.fetchall()


async def get_listening_since(conn):
    return await conn.scalar(select([play.c.date]).order_by(play.c.date.asc()).limit(1))


async def count_per_year(conn):
    year = func.date_part('YEAR', play.c.date).label('year')
    plays = func.count().label('plays')
    result = await conn.execute(select([year, plays]).group_by(year).order_by(year))
    return await result.fetchall()
