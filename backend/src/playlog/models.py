import sqlalchemy as sa


metadata = sa.MetaData()


artist = sa.Table(
    'artist',
    metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(500), nullable=False),
    sa.Column('plays', sa.Integer(), nullable=False),
    sa.Column('first_play', sa.DateTime(), nullable=False),
    sa.Column('last_play', sa.DateTime(), nullable=False)
)


album = sa.Table(
    'album',
    metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('artist_id', sa.ForeignKey('artist.id', ondelete='CASCADE'), nullable=False),
    sa.Column('name', sa.String(500), nullable=False),
    sa.Column('plays', sa.Integer(), nullable=False),
    sa.Column('first_play', sa.DateTime(), nullable=False),
    sa.Column('last_play', sa.DateTime(), nullable=False)
)


track = sa.Table(
    'track',
    metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('album_id', sa.ForeignKey('album.id', ondelete='CASCADE'), nullable=False),
    sa.Column('name', sa.String(500), nullable=False),
    sa.Column('plays', sa.Integer(), nullable=False),
    sa.Column('first_play', sa.DateTime(), nullable=False),
    sa.Column('last_play', sa.DateTime(), nullable=False)
)


play = sa.Table(
    'play',
    metadata,
    sa.Column('track_id', sa.ForeignKey('track.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('date', sa.DateTime(), primary_key=True)
)
