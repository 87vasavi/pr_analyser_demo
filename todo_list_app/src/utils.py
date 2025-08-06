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
    """
    Delete a task by its ID.
    
    Args:
        task_id (int): The ID of the task to delete
        
    Returns:
        bool: True if task was deleted successfully, False if task not found
    """
    if task_id in task_db:
        del task_db[task_id]
        return True
    return False