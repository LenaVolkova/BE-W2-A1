from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

app = FastAPI(
    title="Task Management API",
    description="A simple FastAPI application to manage a list of tasks with search filters, statistics, and database reset functionality.",
    version="1.0.0"
)

# Hardcoded initial list of tasks
INITIAL_TASKS = [
    {"id": 1, "title": "Configure FastAPI project", "done": True},
    {"id": 2, "title": "Implement CRUD endpoints", "done": False},
    {"id": 3, "title": "Test API with Swagger UI", "done": False}
]

# In-memory "database" copy
tasks_db = [t.copy() for t in INITIAL_TASKS]

# Pydantic schemas for request validation
class TaskCreate(BaseModel):
    title: str = Field(..., description="The title of the task")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="The new title of the task")
    done: Optional[bool] = Field(None, description="The new status of the task")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")
        return v.strip() if v is not None else None

# Endpoints
@app.get("/", tags=["General"])
def read_root():
    """
    Get application description.
    """
    return {
        "app_name": "Simple Task Manager API",
        "description": "A lightweight FastAPI application for managing tasks, supporting CRUD operations, status statistics, and full reset capability.",
        "version": "1.0.0",
        "documentation_url": "/docs"
    }

@app.get("/health", tags=["General"])
def health_check():
    """
    Check if the application is running.
    """
    return {"status": "ok"}

@app.get("/tasks", tags=["Tasks"])
def get_tasks(
    search: Optional[str] = Query(None, description="Search term to filter task titles (case-insensitive)"),
    done: Optional[bool] = Query(None, description="Filter tasks by status 'done' (true/false)")
):
    """
    Retrieve the list of tasks.
    If no query parameters are specified, returns the list of all tasks.
    If 'search' or 'done' are specified, returns tasks matching those criteria.
    """
    filtered = tasks_db
    if search is not None:
        filtered = [t for t in filtered if search.lower() in t["title"].lower()]
    if done is not None:
        filtered = [t for t in filtered if t["done"] == done]
    return filtered

@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_task_by_id(task_id: int):
    """
    Retrieve details of a task with the specified ID.
    Raises HTTP 404 if the task is not found.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

@app.post("/task", status_code=201, tags=["Tasks"])
def create_task(task_in: TaskCreate):
    """
    Create a new task.
    The task ID is auto-incremented, and the status 'done' defaults to false.
    """
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": next_id,
        "title": task_in.title,
        "done": False
    }
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, task_in: TaskUpdate):
    """
    Update a task's title and/or completion status by ID.
    Raises HTTP 404 if the task is not found.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            if task_in.title is not None:
                task["title"] = task_in.title
            if task_in.done is not None:
                task["done"] = task_in.done
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):
    """
    Delete a task from the list by ID.
    Raises HTTP 404 if the task is not found.
    """
    for i, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(i)
            return {"message": f"Task with ID {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

@app.get("/stats", tags=["Statistics"])
def get_stats():
    """
    Get statistics: total number of tasks, completed tasks, and pending tasks.
    """
    total = len(tasks_db)
    done_count = sum(1 for t in tasks_db if t["done"])
    not_done_count = total - done_count
    return {
        "total_tasks": total,
        "done_tasks": done_count,
        "not_done_tasks": not_done_count
    }

@app.post("/reset", tags=["Database Control"])
@app.get("/reset", tags=["Database Control"])
def reset_tasks():
    """
    Re-initialize the task database to its initial hardcoded state.
    """
    global tasks_db
    tasks_db = [t.copy() for t in INITIAL_TASKS]
    return {
        "message": "Task database has been reset to the initial state",
        "tasks": tasks_db
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
