from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from src.models import Task, TaskStatus, Subtask
from src.utils import add_task, get_task, get_all_tasks

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
def create_task(title: str, description: str, due_date: Optional[date] = None):
    try:
        task = add_task(title, description, due_date)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tasks/{task_id}/subtasks/", response_model=Subtask)
def create_subtask(task_id: int, title: str, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    subtask = Subtask(title=title, task_id=task_id)
    session.add(subtask)
    session.commit()
    session.refresh(subtask)
    return subtask

@app.patch("/subtasks/{subtask_id}/complete/")
def complete_subtask(subtask_id: int, session: Session = Depends(get_session)):
    subtask = session.get(Subtask, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")

    subtask.completed = True
    session.commit()
    return {"message": "Subtask marked as completed"}
