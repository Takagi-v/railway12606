"""add_all_user_types

Revision ID: 1234567890ab
Revises: f293aa2eacfa
Create Date: 2025-12-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1234567890ab'
down_revision: Union[str, None] = 'f293aa2eacfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    # Check if we are using PostgreSQL
    if conn.dialect.name == 'postgresql':
        # PostgreSQL requires ALTER TYPE to add enum values
        # We use autocommit_block because ALTER TYPE cannot run inside a transaction block 
        # in some configurations or depending on alembic execution mode
        with op.get_context().autocommit_block():
            # Update UserType enum
            op.execute("ALTER TYPE user_type_enum ADD VALUE IF NOT EXISTS '儿童'")
            op.execute("ALTER TYPE user_type_enum ADD VALUE IF NOT EXISTS '残疾军人'")
            
            # Update PassengerType enum
            # '儿童' already exists in PassengerType based on previous code
            op.execute("ALTER TYPE passenger_type_enum ADD VALUE IF NOT EXISTS '残疾军人'")
    else:
        # For SQLite or others that don't enforce native ENUM types strictly or handle it differently
        # Usually no action is needed if the column is just VARCHAR
        pass


def downgrade() -> None:
    # Downgrading enums (removing values) is not directly supported in PostgreSQL
    pass
