"""fix dates

Revision ID: a780c567e119
Revises: 71e790cfae2f
Create Date: 2017-12-21 17:55:25.874510

"""

from alembic import op


revision = 'a780c567e119'
down_revision = '71e790cfae2f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    UPDATE track SET
        first_play = (SELECT MIN(date) FROM play WHERE track_id = track.id),
        last_play = (SELECT MAX(date) FROM play WHERE track_id = track.id)
    ;
    """)
    op.execute("""
    UPDATE album SET
        first_play = (SELECT MIN(first_play) FROM track WHERE album_id = album.id),
        last_play = (SELECT MAX(last_play) FROM track WHERE album_id = album.id)
    ;
    """)
    op.execute("""
    UPDATE artist SET
        first_play = (SELECT MIN(first_play) FROM album WHERE artist_id = artist.id),
        last_play = (SELECT MAX(last_play) FROM album WHERE artist_id = artist.id)
    ;
    """)


def downgrade():
    pass
