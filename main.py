from fastapi import FastAPI, HTTPException
import uvicorn

# Create an app
app = FastAPI()

# Dictionary with tasks instead of db
tasks_db = [
    {"id": 1, "title": "Install FastAPI", "done": False},
    {"id": 2, "title": "Create first endpoint", "done": True},
    {"id": 3, "title": "Add tasks", "done": False}
]

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



# Launch server 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)