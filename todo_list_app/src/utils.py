from src.models import Task, TaskStatus

# Simulated database (Dictionary)
task_db = {}
task_counter = 1

def add_task(title: str, description: str):
    global task_counter
    task = Task(id=task_counter, title=title, description=description)
    task_db[task_counter] = task
    task_counter += 1
    return task

def get_task(task_id: int):
    return task_db.get(task_id)

def get_all_tasks():
    return list(task_db.values())

def delete_task(task_id: int):
    return task_db.pop(task_id, None)
