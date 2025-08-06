from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.models import Task, TaskStatus, TaskCreateRequest
from src.utils import add_task, get_task, get_all_tasks, delete_task

app = FastAPI(title="Task Management API", description="API for managing tasks")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler to return 400 Bad Request for validation errors"""
    # Check if the error is related to description length
    for error in exc.errors():
        if error.get('loc') and 'description' in error.get('loc', []):
            error_type = error.get('type', '')
            # Handle different possible error types for string length validation
            if 'max_length' in error_type or 'too_long' in error_type:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Task description must not exceed 150 characters"}
                )
    
    # For other validation errors, return a generic 400 response
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request data"}
    )

@app.get("/")
def health_check():
    return {"status": "Task Management API is running"}

@app.get("/tasks", tags=["Tasks"])
def list_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}", tags=["Tasks"])
def retrieve_task(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", tags=["Tasks"])
def create_task(task_request: TaskCreateRequest):
    # FastAPI will automatically validate the request using the TaskCreateRequest model
    # If validation fails, our custom exception handler will return 400 Bad Request
    task = add_task(task_request.title, task_request.description)
    return task
