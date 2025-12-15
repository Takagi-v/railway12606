import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Add backend directory to path
current_dir = os.getcwd()
if current_dir.endswith('backend'):
    backend_dir = current_dir
else:
    backend_dir = os.path.join(current_dir, 'backend')

sys.path.append(backend_dir)

# Load environment variables
load_dotenv(os.path.join(backend_dir, '.env'))

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_schema():
    inspector = inspect(engine)
    columns = inspector.get_columns('order_passengers')
    print("Columns in order_passengers:")
    for col in columns:
        print(f"- {col['name']} ({col['type']})")

    print("\nColumns in seats:")
    columns = inspector.get_columns('seats')
    for col in columns:
        print(f"- {col['name']} ({col['type']})")

if __name__ == "__main__":
    check_schema()
