from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
#from typing import Optional
import uvicorn

# Create an app
app = FastAPI()

# Dictionary with tasks instead of db
tasks_db = [
    {"id": 1, "title": "Install FastAPI", "done": False},
    {"id": 2, "title": "Create first endpoint", "done": True},
    {"id": 3, "title": "Add tasks", "done": False}
]

class TaskCreate(BaseModel):
    title: str

# Validation for update (PUT)
class UpdateTaskModel(BaseModel):
    # Field(..., min_length=1) is to ensure that the string is not empty.
    # "Optional" allows to update "title" or "done", or both.
    title: str | None = Field(None, min_length=1, description="Task's title cannot be empty")
    done: bool | None = Field(None, description="Status of the task")

# Configure root path - retutn API description
@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

#Endpoint to check that server is working
@app.get("/health")
def get_info():
    return { "status": "ok" }

# Endpoint to get tasks list
@app.get("/tasks")
def get_tasks():
    return tasks_db

#Endpoint to get a task by id
@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
            
    # If there is no task with such a number, then return 404 error code
    raise HTTPException(status_code=404, detail="Task not found")

#Enpoint for adding new task
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    # Delete spaces from string's ends
    clean_title = task_data.title.strip()
    
    # If the title is not empty
    if not clean_title:
        raise HTTPException(
            status_code=400, 
            detail="Title cannot be empty or contain only spaces"
        )
    
    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    
    new_task = {
        "id": new_id,
        "title": clean_title,  
        "done": False              
    }
    
    tasks_db.append(new_task)
    return new_task

# How to test:
#curl -i -X POST http://localhost:8000/tasks \     
#     -H "Content-Type: application/json" \
#     -d '{"title": "    "}'
#HTTP/1.1 400 Bad Request
#date: Mon, 20 Jul 2026 11:35:59 GMT
#server: uvicorn
#content-length: 57
#content-type: application/json
#{"detail":"Title cannot be empty or contain only spaces"}% 

#curl -i -X POST http://localhost:8000/tasks \ 
#     -H "Content-Type: application/json" \
#     -d '{"title": "Buy milk"}'
#HTTP/1.1 201 Created
#date: Mon, 20 Jul 2026 11:36:29 GMT
#server: uvicorn
#content-length: 40
#content-type: application/json
#{"id":4,"title":"Buy milk","done":false}%


### Endpoint PUT /tasks/{id}
@app.put("/tasks/{id}")
async def update_task(id: int, task_body: UpdateTaskModel):
    task = next((t for t in tasks_db if t["id"] == id), None)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {id} not found"
        )
    
    update_data = task_body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Body cannot be empty. Provide 'title' or 'done'."
        )
    
    if "title" in update_data:
        task["title"] = update_data["title"]
    if "done" in update_data:
        task["done"] = update_data["done"]
        
    return task


### Endpoint DELETE /tasks/{id}
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    task = next((t for t in tasks_db if t["id"] == id), None)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {id} not found"
        )
        
    tasks_db.remove(task)
    
    # 4. Returns None (FastAPI creates response 204 "no content" automatically)
    return None

# in order to test PUT and DELETE following curl-strings can be used:
# curl -X PUT "http://localhost:8000/tasks/4" -H "Content-Type: application/json" -d '{"title": "Byu milk and eggs", "done": true}'
# curl -i -X DELETE http://localhost:8000/tasks/4 

# Launch server 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
