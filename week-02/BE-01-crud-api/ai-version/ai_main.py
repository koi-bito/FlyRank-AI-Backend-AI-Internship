"""
AI Rematch Code — Built from memory prompt:
"Write a FastAPI task manager with CRUD endpoints, in-memory list, 404 on missing tasks, and 400 on empty titles."
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AI Generated Task API")

tasks = [
    {"id": 1, "title": "AI Task 1", "done": False},
    {"id": 2, "title": "AI Task 2", "done": True},
]

class TaskItem(BaseModel):
    title: str
    done: Optional[bool] = False

@app.get("/")
def home():
    return {"message": "AI Task API"}

@app.get("/tasks")
def list_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskItem):
    # Notice: Standard AI code often relies on Pydantic and forgets to reject whitespace-only strings
    # or raises 422 Unprocessable Entity instead of 400 Bad Request if validation fails
    new_id = len(tasks) + 1
    new_task = {"id": new_id, "title": task.title, "done": task.done}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskItem):
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            t["done"] = task.done
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Task not found")
