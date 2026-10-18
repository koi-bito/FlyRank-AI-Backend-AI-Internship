from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

class TaskRepository(ABC):
    """Abstract interface defining the Task persistence contract."""
    
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def create(self, title: str) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass


class PostgresTaskRepository(TaskRepository):
    """PostgreSQL implementation for Docker container environment."""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._init_db()

    def _get_connection(self):
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            done BOOLEAN NOT NULL DEFAULT FALSE,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    cur.execute("SELECT COUNT(*) as count FROM tasks;")
                    row = cur.fetchone()
                    if row and row["count"] == 0:
                        cur.execute("""
                            INSERT INTO tasks (title, done) VALUES 
                            ('Review FL-01 workflow audit', TRUE),
                            ('Build BE-01 CRUD API with FastAPI', TRUE),
                            ('Containerize Postgres Stack for BE-04', FALSE);
                        """)
                conn.commit()
        except Exception as e:
            print(f"Postgres init notice (may be initializing via Docker entrypoint): {e}")

    def get_all(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done, created_at FROM tasks ORDER BY id ASC;")
                rows = cur.fetchall()
                return [dict(r) for r in rows]

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done, created_at FROM tasks WHERE id = %s;", (task_id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def create(self, title: str) -> Dict[str, Any]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done, created_at;",
                    (title,)
                )
                created = cur.fetchone()
                conn.commit()
                return dict(created)

    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done, created_at FROM tasks WHERE id = %s;", (task_id,))
                existing = cur.fetchone()
                if not existing:
                    return None
                
                new_title = title if title is not None else existing["title"]
                new_done = done if done is not None else existing["done"]
                
                cur.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done, created_at;",
                    (new_title, new_done, task_id)
                )
                updated = cur.fetchone()
                conn.commit()
                return dict(updated)

    def delete(self, task_id: int) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
                deleted = cur.fetchone()
                conn.commit()
                return deleted is not None


class SQLiteTaskRepository(TaskRepository):
    """SQLite implementation acting as the fallback/local store."""
    
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tasks;")
        count = cur.fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?);",
                [
                    ("Review FL-01 workflow audit", 1),
                    ("Build BE-01 CRUD API with FastAPI", 1),
                    ("Containerize Postgres Stack for BE-04", 0)
                ]
            )
        conn.commit()
        conn.close()

    def get_all(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, done, created_at FROM tasks ORDER BY id ASC;")
        res = [{"id": r["id"], "title": r["title"], "done": bool(r["done"]), "created_at": r["created_at"]} for r in cur.fetchall()]
        conn.close()
        return res

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, done, created_at FROM tasks WHERE id = ?;", (task_id,))
        row = cur.fetchone()
        conn.close()
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "created_at": row["created_at"]} if row else None

    def create(self, title: str) -> Dict[str, Any]:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, 0);", (title,))
        new_id = cur.lastrowid
        conn.commit()
        cur.execute("SELECT id, title, done, created_at FROM tasks WHERE id = ?;", (new_id,))
        row = cur.fetchone()
        res = {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "created_at": row["created_at"]}
        conn.close()
        return res

    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, done FROM tasks WHERE id = ?;", (task_id,))
        existing = cur.fetchone()
        if not existing:
            conn.close()
            return None
        new_title = title if title is not None else existing["title"]
        new_done = (1 if done else 0) if done is not None else existing["done"]
        cur.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?;", (new_title, new_done, task_id))
        conn.commit()
        cur.execute("SELECT id, title, done, created_at FROM tasks WHERE id = ?;", (task_id,))
        row = cur.fetchone()
        res = {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "created_at": row["created_at"]}
        conn.close()
        return res

    def delete(self, task_id: int) -> bool:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        affected = cur.rowcount
        conn.commit()
        conn.close()
        return affected > 0
