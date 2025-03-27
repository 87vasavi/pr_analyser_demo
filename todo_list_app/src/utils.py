from models import Task, TaskStatus
from datetime import date
from typing import Dict


# Simulated database
task_db: Dict[int, Task] = {}
task_counter = 1

def add_task(title: str, description: str, due_date: Optional[date] = None):
    global task_counter

    # Validate due date
    if due_date and due_date < date.today():
        raise ValueError("Due date cannot be in the past.")

    task = Task(id=task_counter, title=title, description=description, due_date=due_date)
    task_db[task_counter] = task
    task_counter += 1
    return task

def get_task(task_id: int):
    return task_db.get(task_id)

def get_all_tasks():
    return list(task_db.values())
