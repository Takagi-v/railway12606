"""DB completion: enums, constraints, indexes

Revision ID: 9b54f2f7d0dc
Revises: 5c6563c7ae29
Create Date: 2025-11-02 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b54f2f7d0dc'
down_revision: Union[str, None] = '5c6563c7ae29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types if not exist (PostgreSQL-specific)
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'id_type_enum') THEN
        CREATE TYPE id_type_enum AS ENUM ('身份证', '护照', '港澳通行证', '台胞证');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type_enum') THEN
        CREATE TYPE user_type_enum AS ENUM ('成人', '学生');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'passenger_type_enum') THEN
        CREATE TYPE passenger_type_enum AS ENUM ('成人', '学生', '儿童');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'train_type_enum') THEN
        CREATE TYPE train_type_enum AS ENUM ('高铁', '动车', '直达');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'seat_type_enum') THEN
        CREATE TYPE seat_type_enum AS ENUM ('一等座', '二等座', '软卧', '硬卧');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'seat_status_enum') THEN
        CREATE TYPE seat_status_enum AS ENUM ('可售', '已锁定', '已售');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status_enum') THEN
        CREATE TYPE order_status_enum AS ENUM ('待支付', '已支付', '已取消', '已退票');
    END IF;
END $$;
""")
    op.execute("""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'refund_status_enum') THEN
        CREATE TYPE refund_status_enum AS ENUM ('未退票', '已退票');
    END IF;
END $$;
""")

    # Alter column types from VARCHAR to corresponding ENUMs (PostgreSQL-specific casts)
    op.execute("ALTER TABLE users ALTER COLUMN id_type TYPE id_type_enum USING id_type::id_type_enum;")
    op.execute("ALTER TABLE users ALTER COLUMN user_type TYPE user_type_enum USING user_type::user_type_enum;")

    op.execute("ALTER TABLE passengers ALTER COLUMN id_type TYPE id_type_enum USING id_type::id_type_enum;")
    op.execute("ALTER TABLE passengers ALTER COLUMN passenger_type TYPE passenger_type_enum USING passenger_type::passenger_type_enum;")

    op.execute("ALTER TABLE trains ALTER COLUMN train_type TYPE train_type_enum USING train_type::train_type_enum;")

    op.execute("ALTER TABLE seats ALTER COLUMN seat_type TYPE seat_type_enum USING seat_type::seat_type_enum;")
    op.execute("ALTER TABLE seats ALTER COLUMN status TYPE seat_status_enum USING status::seat_status_enum;")

    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE order_status_enum USING status::order_status_enum;")

    op.execute("ALTER TABLE order_passengers ALTER COLUMN ticket_type TYPE passenger_type_enum USING ticket_type::passenger_type_enum;")
    op.execute("ALTER TABLE order_passengers ALTER COLUMN seat_type TYPE seat_type_enum USING seat_type::seat_type_enum;")
    op.execute("ALTER TABLE order_passengers ALTER COLUMN refund_status TYPE refund_status_enum USING refund_status::refund_status_enum;")

    # Users: replace unique index on id_number with composite unique constraint (id_type, id_number)
    op.execute("DROP INDEX IF EXISTS ix_users_id_number;")
    op.execute("ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS uix_user_idtype_idnumber UNIQUE (id_type, id_number);")
    # Recreate non-unique index on id_number for lookup efficiency
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_id_number ON users (id_number);")

    # Passenger: update unique constraint to include id_type
    op.execute("ALTER TABLE passengers DROP CONSTRAINT IF EXISTS uix_user_passenger;")
    op.execute("ALTER TABLE passengers ADD CONSTRAINT IF NOT EXISTS uix_user_passenger UNIQUE (user_id, id_type, id_number);")

    # Seat: enforce uniqueness of seat per train/date/type/number
    op.execute("ALTER TABLE seats ADD CONSTRAINT IF NOT EXISTS uix_seat_unique UNIQUE (train_id, travel_date, seat_type, seat_number);")

    # Train: route index for departure/arrival
    op.execute("CREATE INDEX IF NOT EXISTS ix_train_route ON trains (departure_station_id, arrival_station_id);")

    # Orders: composite index and non-negative total price constraint
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_user_status_date ON orders (user_id, status, create_time);")
    op.execute("ALTER TABLE orders ADD CONSTRAINT IF NOT EXISTS ck_order_total_price_nonnegative CHECK (total_price >= 0);")

    # OrderPassengers: non-negative price constraint
    op.execute("ALTER TABLE order_passengers ADD CONSTRAINT IF NOT EXISTS ck_order_passenger_price_nonnegative CHECK (price >= 0);")

    # Stations: unique aliases for search determinism
    op.execute("ALTER TABLE stations ADD CONSTRAINT IF NOT EXISTS uix_station_pinyin UNIQUE (pinyin);")
    op.execute("ALTER TABLE stations ADD CONSTRAINT IF NOT EXISTS uix_station_short_pinyin UNIQUE (short_pinyin);")


def downgrade() -> None:
    # Drop station unique constraints
    op.execute("ALTER TABLE stations DROP CONSTRAINT IF EXISTS uix_station_short_pinyin;")
    op.execute("ALTER TABLE stations DROP CONSTRAINT IF EXISTS uix_station_pinyin;")

    # Drop order passengers price check
    op.execute("ALTER TABLE order_passengers DROP CONSTRAINT IF EXISTS ck_order_passenger_price_nonnegative;")

    # Drop orders index and check constraint
    op.execute("ALTER TABLE orders DROP CONSTRAINT IF EXISTS ck_order_total_price_nonnegative;")
    op.execute("DROP INDEX IF EXISTS ix_orders_user_status_date;")

    # Drop train route index
    op.execute("DROP INDEX IF EXISTS ix_train_route;")

    # Drop seat unique constraint
    op.execute("ALTER TABLE seats DROP CONSTRAINT IF EXISTS uix_seat_unique;")

    # Restore passenger unique constraint to previous (user_id, id_number) only
    op.execute("ALTER TABLE passengers DROP CONSTRAINT IF EXISTS uix_user_passenger;")
    op.execute("ALTER TABLE passengers ADD CONSTRAINT uix_user_passenger UNIQUE (user_id, id_number);")

    # Users: drop composite unique and recreate previous unique index
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS uix_user_idtype_idnumber;")
    op.execute("DROP INDEX IF EXISTS ix_users_id_number;")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_id_number ON users (id_number);")

    # Revert enum columns back to VARCHAR
    op.execute("ALTER TABLE order_passengers ALTER COLUMN refund_status TYPE VARCHAR(20) USING refund_status::text;")
    op.execute("ALTER TABLE order_passengers ALTER COLUMN seat_type TYPE VARCHAR(20) USING seat_type::text;")
    op.execute("ALTER TABLE order_passengers ALTER COLUMN ticket_type TYPE VARCHAR(20) USING ticket_type::text;")

    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE VARCHAR(20) USING status::text;")

    op.execute("ALTER TABLE seats ALTER COLUMN status TYPE VARCHAR(20) USING status::text;")
    op.execute("ALTER TABLE seats ALTER COLUMN seat_type TYPE VARCHAR(20) USING seat_type::text;")

    op.execute("ALTER TABLE trains ALTER COLUMN train_type TYPE VARCHAR(10) USING train_type::text;")

    op.execute("ALTER TABLE passengers ALTER COLUMN passenger_type TYPE VARCHAR(20) USING passenger_type::text;")
    op.execute("ALTER TABLE passengers ALTER COLUMN id_type TYPE VARCHAR(20) USING id_type::text;")

    op.execute("ALTER TABLE users ALTER COLUMN user_type TYPE VARCHAR(20) USING user_type::text;")
    op.execute("ALTER TABLE users ALTER COLUMN id_type TYPE VARCHAR(20) USING id_type::text;")

    # Drop enum types (safe if not referenced)
    op.execute("DROP TYPE IF EXISTS refund_status_enum;")
    op.execute("DROP TYPE IF EXISTS order_status_enum;")
    op.execute("DROP TYPE IF EXISTS seat_status_enum;")
    op.execute("DROP TYPE IF EXISTS seat_type_enum;")
    op.execute("DROP TYPE IF EXISTS train_type_enum;")
    op.execute("DROP TYPE IF EXISTS passenger_type_enum;")
    op.execute("DROP TYPE IF EXISTS user_type_enum;")
    op.execute("DROP TYPE IF EXISTS id_type_enum;")