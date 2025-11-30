import sqlite3
import bcrypt

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

db_path = r'backend/test_railway.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    username = 'gptuser20251114'
    new_password = '123456'
    hashed_password = get_password_hash(new_password)
    
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    
    print(f"Updated password for {username} to '{new_password}'")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
