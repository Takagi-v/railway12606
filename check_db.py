import sqlite3
import os

db_path = r'backend/test_railway.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    
    # Try to find a users table (guessing name 'user' or 'users')
    user_table = None
    for t in tables:
        if 'user' in t[0].lower():
            user_table = t[0]
            break
            
    if user_table:
        print(f"Found user table: {user_table}")
        # Get columns
        cursor.execute(f"PRAGMA table_info({user_table})")
        columns = cursor.fetchall()
        print(f"Columns: {[c[1] for c in columns]}")
        
        # Get one user
        cursor.execute(f"SELECT * FROM {user_table} LIMIT 1")
        user = cursor.fetchone()
        print("User:", user)
    else:
        print("No user table found")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
