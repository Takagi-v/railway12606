"""add partially refunded status

Revision ID: a3cf3f1174a5
Revises: 9362d537fa21
Create Date: 2025-12-07 21:17:34.589987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3cf3f1174a5'
down_revision: Union[str, None] = '9362d537fa21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

