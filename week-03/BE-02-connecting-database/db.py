import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "tasks.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Check if table is empty; insert initial 3 tasks only if empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        initial_tasks = [
            ("Review FL-01 workflow audit", 1),
            ("Build BE-01 CRUD API with FastAPI", 1),
            ("Configure SQLite persistence for BE-02", 0),
        ]
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", initial_tasks)
        conn.commit()
        print("Database initialized with 3 default tasks.")
    else:
        print(f"Database already exists with {count} tasks. Skipping seed.")
        
    conn.close()

if __name__ == "__main__":
    init_db()
