from fastapi import FastAPI, HTTPException, status, Response, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Task API — In-Memory CRUD Engine",
    description="Full CRUD Task Management REST API with validation, Swagger UI documentation, filtering, search, and stats endpoints.",
    version="1.0.0"
)

# Pydantic Schemas for OpenAPI / Swagger UI documentation
class Task(BaseModel):
    id: int = Field(..., description="Unique integer ID of the task", example=1)
    title: str = Field(..., description="Descriptive title of the task", example="Build CRUD API")
    done: bool = Field(..., description="Whether the task has been completed", example=False)

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Title for the new task (required, non-empty)", example="Buy milk")

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Updated task title", example="Buy almond milk")
    done: Optional[bool] = Field(None, description="Updated completion status", example=True)

class TaskStatsResponse(BaseModel):
    total: int = Field(..., example=3)
    done: int = Field(..., example=1)
    open: int = Field(..., example=2)

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Task 99 not found")

# Initial seed data
INITIAL_TASKS = [
    {"id": 1, "title": "Review FL-01 workflow audit", "done": True},
    {"id": 2, "title": "Build BE-01 CRUD API with FastAPI", "done": False},
    {"id": 3, "title": "Configure SQLite persistence for BE-02", "done": False},
]

tasks = [dict(t) for t in INITIAL_TASKS]

@app.get(
    "/",
    summary="API Root Information",
    description="Returns metadata about the API and available entry points.",
    tags=["General"]
)
def get_root():
    return {
        "name": "Task API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"]
    }

@app.get(
    "/health",
    summary="Health Check Probe",
    description="Lightweight liveness probe returning ok status.",
    tags=["General"]
)
def get_health():
    return {"status": "ok"}

@app.get(
    "/tasks",
    response_model=List[Task],
    summary="List All Tasks",
    description="Retrieve all tasks, optionally filtered by status ('done') or searched by keyword ('search').",
    tags=["Tasks"]
)
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status (true/false)"),
    search: Optional[str] = Query(None, description="Search tasks by keyword in the title")
):
    results = tasks
    if done is not None:
        results = [t for t in results if t["done"] is done]
    if search:
        keyword = search.lower()
        results = [t for t in results if keyword in t["title"].lower()]
    return results

@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    responses={404: {"model": ErrorResponse, "description": "Task not found"}},
    summary="Get Task by ID",
    description="Retrieve a single task by its unique integer identifier.",
    tags=["Tasks"]
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Task {task_id} not found"}
    )

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse, "description": "Missing or invalid title"}},
    summary="Create New Task",
    description="Create a new task with an auto-assigned incremental ID and default done=false.",
    tags=["Tasks"]
)
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
    
    next_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid update payload"},
        404: {"model": ErrorResponse, "description": "Task not found"}
    },
    summary="Update Existing Task",
    description="Update the title and/or completion state of an existing task.",
    tags=["Tasks"]
)
async def update_task(task_id: int, payload: dict):
    target = None
    for task in tasks:
        if task["id"] == task_id:
            target = task
            break
            
    if not target:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
        
    if not payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Update payload cannot be empty"}
        )
        
    if "title" in payload:
        title = str(payload["title"]).strip()
        if not title:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Title cannot be empty"}
            )
        target["title"] = title
        
    if "done" in payload:
        if not isinstance(payload["done"], bool):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "'done' field must be a boolean"}
            )
        target["done"] = payload["done"]
        
    return target

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse, "description": "Task not found"}},
    summary="Delete Task",
    description="Remove a task from the in-memory collection by its integer ID.",
    tags=["Tasks"]
)
def delete_task(task_id: int):
    target_idx = None
    for idx, task in enumerate(tasks):
        if task["id"] == task_id:
            target_idx = idx
            break
            
    if target_idx is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
        
    tasks.pop(target_idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get(
    "/stats",
    response_model=TaskStatsResponse,
    summary="Task Aggregate Statistics",
    description="Returns aggregate counts of total, completed, and pending tasks.",
    tags=["General"]
)
def get_stats():
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    return {
        "total": total,
        "done": done_count,
        "open": total - done_count
    }

@app.post(
    "/reset",
    summary="Reset In-Memory State",
    description="Resets the in-memory tasks to the original 3 initial seed tasks.",
    tags=["General"]
)
def reset_tasks():
    global tasks
    tasks = [dict(t) for t in INITIAL_TASKS]
    return {"message": "Tasks reset to initial seed state", "count": len(tasks)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
