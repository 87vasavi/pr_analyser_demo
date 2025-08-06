from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.models import Task, TaskStatus, TaskCreateRequest
from src.utils import add_task, get_task, get_all_tasks

app = FastAPI(title="Task Management API", description="API for managing tasks")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler to convert 422 validation errors to 400 Bad Request
    as required by the acceptance criteria
    """
    # Extract validation error details
    errors = exc.errors()
    
    # Check if any error is related to description length
    for error in errors:
        if 'description' in str(error.get('loc', [])) and 'max_length' in error.get('type', ''):
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Task description must not exceed 150 characters"
                }
            )
    
    # For other validation errors, return a generic 400 error
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Validation error: " + str(errors[0].get('msg', 'Invalid input'))
        }
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
    task = add_task(task_request.title, task_request.description)
    return task
