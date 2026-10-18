"""
Stage 4: Learn your first SQL — SQLite Queries and Verification Script
"""
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "tasks.db")

def run_sql_exploration():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("--- 1. SELECT * FROM tasks ---")
    cursor.execute("SELECT id, title, done, created_at FROM tasks;")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Title: {row[1]} | Done: {bool(row[2])} | CreatedAt: {row[3]}")
        
    print("\n--- 2. SELECT * FROM tasks WHERE done = 1 ---")
    cursor.execute("SELECT id, title, done FROM tasks WHERE done = 1;")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Title: {row[1]} | Done: {bool(row[2])}")
        
    print("\n--- 3. SELECT COUNT(*) FROM tasks ---")
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    count = cursor.fetchone()[0]
    print(f"Total task count: {count}")
    
    print("\n--- 4. SELECT COUNT(*) as completed_count FROM tasks WHERE done = 1 ---")
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1;")
    completed = cursor.fetchone()[0]
    print(f"Completed task count: {completed}")
    
    print("\n--- 5. Search with LIKE: SELECT * FROM tasks WHERE title LIKE '%FastAPI%' ---")
    cursor.execute("SELECT id, title FROM tasks WHERE title LIKE ?;", ('%FastAPI%',))
    for row in cursor.fetchall():
        print(f"Match: ID {row[0]} -> {row[1]}")

    conn.close()
    print("\nSQL Exploration completed successfully!")

if __name__ == "__main__":
    run_sql_exploration()
