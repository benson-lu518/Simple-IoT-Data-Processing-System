import sqlite3

DB_NAME = "devices.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                deviceId TEXT PRIMARY KEY,
                username TEXT NOT NULL
            )
        """)
