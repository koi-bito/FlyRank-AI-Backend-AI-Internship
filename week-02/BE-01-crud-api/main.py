from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="Task API", version="1.0")

# In-memory database of tasks
tasks = [
    {"id": 1, "title": "Review FL-01 workflow audit", "done": True},
    {"id": 2, "title": "Build BE-01 CRUD API with FastAPI", "done": False},
    {"id": 3, "title": "Configure SQLite persistence for BE-02", "done": False},
]

@app.get("/")
def get_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health"]
    }

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Task {task_id} not found"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
