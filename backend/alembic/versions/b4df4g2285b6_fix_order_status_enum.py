"""fix order status enum

Revision ID: b4df4g2285b6
Revises: a3cf3f1174a5
Create Date: 2025-12-07 21:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b4df4g2285b6'
down_revision = 'a3cf3f1174a5'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Postgres 12+ supports ALTER TYPE ADD VALUE in transaction
    op.execute("ALTER TYPE order_status_enum ADD VALUE IF NOT EXISTS '部分退票'")

def downgrade() -> None:
    # Cannot remove enum value easily in Postgres
    pass
