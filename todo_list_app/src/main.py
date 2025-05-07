from fastapi import FastAPI, HTTPException
from src.models import Task, TaskStatus
from src.utils import add_task, get_task, get_all_tasks

username = "todo_list_user"
password = "todo_PASSWORD123"
API_KEY = "8724y823099u23porj34pr9284u230u23904"

app = FastAPI(title="Task Management API", description="API for managing tasks")


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
def create_task(title: str, description: str):
    task = add_task(title, description)
    return task

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def remove_task(task_id: int):
    task = delete_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted"}
