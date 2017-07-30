"""init

Revision ID: 33f9c90c5a0a
Revises:
Create Date: 2017-07-30 16:53:04.475407

"""

import sqlalchemy as sa

from alembic import op


revision = '33f9c90c5a0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'artist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=False),
        sa.Column('plays', sa.Integer(), nullable=False),
        sa.Column('first_play', sa.DateTime(), nullable=False),
        sa.Column('last_play', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'album',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=False),
        sa.Column('plays', sa.Integer(), nullable=False),
        sa.Column('first_play', sa.DateTime(), nullable=False),
        sa.Column('last_play', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'track',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('album_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=False),
        sa.Column('plays', sa.Integer(), nullable=False),
        sa.Column('first_play', sa.DateTime(), nullable=False),
        sa.Column('last_play', sa.DateTime(), nullable=False),
        sa.Column('is_favorite', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['album_id'], ['album.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'play',
        sa.Column('track_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['track_id'], ['track.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('track_id', 'date')
    )


def downgrade():
    op.drop_table('play')
    op.drop_table('track')
    op.drop_table('album')
    op.drop_table('artist')
