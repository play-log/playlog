"""drop track.is_favorite column

Revision ID: 71e790cfae2f
Revises: 33f9c90c5a0a
Create Date: 2017-08-29 17:39:37.850828

"""

import sqlalchemy as sa

from alembic import op


revision = '71e790cfae2f'
down_revision = '33f9c90c5a0a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('track', 'is_favorite')


def downgrade():
    op.add_column('track', sa.Column('is_favorite', sa.Boolean(), nullable=False))
