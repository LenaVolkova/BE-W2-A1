# Task Management API

A simple FastAPI application to manage a list of tasks with search filters, statistics, and database reset functionality. This project is built completely from scratch using FastAPI and Uvicorn.

## Features

- **Hardcoded Initial Tasks**: Pre-populated with 3 default tasks.
- **Root Description & Health Check**: Instantly verify if the server is healthy.
- **Robust Searching and Filtering**: Filter tasks by title content (substring search) and/or completion status (`done`).
- **Complete CRUD Operations**: Create (`POST /task`), Read (`GET /tasks/{id}`), Update (`PUT /tasks/{id}`), and Delete (`DELETE /tasks/{id}`).
- **Statistics**: Retrieve current statistics on completed and pending tasks (`GET /stats`).
- **Reset State**: Clear modifications and restore the hardcoded sample tasks at any time (`POST /reset` or `GET /reset`).

---

## Getting Started

### 1. Installation

Ensure you have Python 3.8+ installed. Install the necessary dependencies (FastAPI and Uvicorn) via `pip`:

```bash
pip install fastapi uvicorn
```

### 2. Running the Application Locally

Run the Uvicorn development server from the project directory:

```bash
python main.py
```

Alternatively, you can start it using the Uvicorn CLI command:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Once running, the application is accessible at:
- API Base URL: `http://127.0.0.1:8000`
- Interactive API Docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative API Docs (ReDoc): `http://127.0.0.1:8000/redoc`

---

## How to Use Swagger UI

FastAPI automatically generates interactive API documentation. To view and interact with the endpoints:

1. Open your web browser and navigate to `http://127.0.0.1:8000/docs`.
2. You will see a list of categorized endpoints: **General**, **Tasks**, **Statistics**, and **Database Control**.
3. Click on any endpoint block to expand it.
4. Click the **"Try it out"** button in the top right of the expanded view.
5. Fill in any required parameters (like `task_id` or query parameters) or request bodies.
6. Click the blue **"Execute"** button to send the request. Swagger UI will display the request URL, headers, response status code, and the response body.

---

## Endpoint Guide & Example Curl Commands

### 1. Root / Application Description
- **URL**: `GET /`
- **Description**: Returns general information about the application.
- **Example request**:
  ```bash
  curl http://127.0.0.1:8000/
  ```

### 2. Health Check
- **URL**: `GET /health`
- **Description**: Verifies if the application is running successfully.
- **Example request**:
  ```bash
  curl http://127.0.0.1:8000/health
  ```

### 3. List Tasks (with optional filtering)
- **URL**: `GET /tasks`
- **Parameters**: 
  - `search` (string, optional): filters tasks whose titles contain the string.
  - `done` (boolean, optional): filters tasks by status (`true` / `false`).
- **Example requests**:
  - Get all tasks:
    ```bash
    curl http://127.0.0.1:8000/tasks
    ```
  - Get tasks matching a search term:
    ```bash
    curl "http://127.0.0.1:8000/tasks?search=FastAPI"
    ```
  - Get completed tasks:
    ```bash
    curl "http://127.0.0.1:8000/tasks?done=true"
    ```
  - Get pending tasks matching search:
    ```bash
    curl "http://127.0.0.1:8000/tasks?search=endpoints&done=false"
    ```

### 4. Get Task Details
- **URL**: `GET /tasks/{id}`
- **Description**: Retrieves detailed information for a task by ID. Returns HTTP 404 if it does not exist.
- **Example request**:
  ```bash
  curl http://127.0.0.1:8000/tasks/1
  ```

### 5. Create Task
- **URL**: `POST /task`
- **Description**: Creates a new task. The `id` is auto-assigned, and `done` defaults to `false`.
- **Request Body**: JSON containing `title`.
- **Example request**:
  ```bash
  curl -X POST http://127.0.0.1:8000/task \
       -H "Content-Type: application/json" \
       -d '{"title": "Read advanced FastAPI guides"}'
  ```

### 6. Update Task
- **URL**: `PUT /tasks/{id}`
- **Description**: Updates the task's `title` and/or `done` status. Returns HTTP 404 if the task doesn't exist.
- **Request Body**: JSON containing optional `title` and `done` values.
- **Example request**:
  ```bash
  curl -X PUT http://127.0.0.1:8000/tasks/2 \
       -H "Content-Type: application/json" \
       -d '{"title": "Implement CRUD endpoints thoroughly", "done": true}'
  ```

### 7. Delete Task
- **URL**: `DELETE /tasks/{id}`
- **Description**: Removes the task from the list. Returns HTTP 404 if not found.
- **Example request**:
  ```bash
  curl -X DELETE http://127.0.0.1:8000/tasks/3
  ```

### 8. Statistics
- **URL**: `GET /stats`
- **Description**: Shows the total count of tasks, completed tasks, and pending (not done) tasks.
- **Example request**:
  ```bash
  curl http://127.0.0.1:8000/stats
  ```

### 9. Reset Tasks
- **URL**: `POST /reset` (or `GET /reset`)
- **Description**: Restores the database back to the 3 original hardcoded tasks.
- **Example request**:
  ```bash
  curl -X POST http://127.0.0.1:8000/reset
  ```
