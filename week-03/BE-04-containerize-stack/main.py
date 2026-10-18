import os
from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from repository import TaskRepository, PostgresTaskRepository, SQLiteTaskRepository

app = FastAPI(
    title="Containerized Task API",
    description="Multi-engine REST Task API supporting PostgreSQL in Docker with zero-change repository swapping.",
    version="1.0.0"
)

def get_repository() -> TaskRepository:
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres"):
        return PostgresTaskRepository(database_url)
    db_file = os.getenv("SQLITE_DB", "tasks.db")
    return SQLiteTaskRepository(db_file)

@app.get("/")
def get_root():
    db_type = "PostgreSQL (Docker)" if os.getenv("DATABASE_URL") else "SQLite"
    return {
        "name": "Containerized Task API",
        "version": "1.0.0",
        "engine": db_type,
        "docs": "/docs",
        "endpoints": ["/tasks", "/health"]
    }

@app.get("/health")
def get_health(repo: TaskRepository = Depends(get_repository)):
    try:
        # Check DB liveness by running a quick count
        repo.get_all()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "error", "database": str(e)}
        )

@app.get("/tasks")
def get_tasks(repo: TaskRepository = Depends(get_repository)):
    return repo.get_all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int, repo: TaskRepository = Depends(get_repository)):
    task = repo.get_by_id(task_id)
    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: dict, repo: TaskRepository = Depends(get_repository)):
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
    return repo.create(title)

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, payload: dict, repo: TaskRepository = Depends(get_repository)):
    if not payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Update payload cannot be empty"}
        )
    title = None
    if "title" in payload:
        title = str(payload["title"]).strip()
        if not title:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Title cannot be empty"}
            )
            
    done = None
    if "done" in payload:
        if not isinstance(payload["done"], bool):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "'done' field must be a boolean"}
            )
        done = payload["done"]
        
    updated = repo.update(task_id, title=title, done=done)
    if not updated:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
    return updated

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, repo: TaskRepository = Depends(get_repository)):
    deleted = repo.delete(task_id)
    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
