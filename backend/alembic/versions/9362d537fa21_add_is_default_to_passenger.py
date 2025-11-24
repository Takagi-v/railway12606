"""add_is_default_to_passenger

Revision ID: 9362d537fa21
Revises: fe66341fe85b
Create Date: 2025-11-24 13:37:30.801052

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9362d537fa21'
down_revision: Union[str, None] = 'fe66341fe85b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_default column to passengers table
    op.add_column('passengers', sa.Column('is_default', sa.Boolean(), nullable=False, server_default='false', comment='是否为用户本人的默认乘车人'))


def downgrade() -> None:
    # Remove is_default column from passengers table
    op.drop_column('passengers', 'is_default')

