from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from db import get_db_connection, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Task API — SQLite Persistence", version="1.0.0", lifespan=lifespan)

@app.get("/")
def get_root():
    return {
        "name": "Task API (SQLite)",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/tasks", "/health"]
    }

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done, created_at FROM tasks ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r["id"], "title": r["title"], "done": bool(r["done"]), "created_at": r["created_at"]} for r in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done, created_at FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "created_at": row["created_at"]}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: dict):
    if not payload or "title" not in payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Title is required"}
        )
    title = str(payload.get("title", "")).strip()
    if not title:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Title cannot be empty"}
        )
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
    conn.commit()
    new_id = cursor.lastrowid
    
    cursor.execute("SELECT id, title, done, created_at FROM tasks WHERE id = ?", (new_id,))
    created = cursor.fetchone()
    conn.close()
    
    return {
        "id": created["id"],
        "title": created["title"],
        "done": bool(created["done"]),
        "created_at": created["created_at"]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
