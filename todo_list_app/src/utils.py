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


def update_task(task_id: int, title: str, description: str, status: TaskStatus):
    if task_id not in task_db:
        return None
    task_db[task_id].title = title
    task_db[task_id].description = description
    task_db[task_id].status = status
    return task_db[task_id]
