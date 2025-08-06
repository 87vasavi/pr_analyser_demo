import pytest
from src.utils import add_task, get_task, get_all_tasks, delete_task, task_db, task_counter

def setup_function():
    """Reset the task database before each test"""
    global task_counter
    task_db.clear()
    task_counter = 1

def test_delete_task_existing():
    """Test delete_task function with existing task"""
    # Add a task
    task = add_task("Test Task", "Test Description")
    task_id = task.id
    
    # Verify task exists
    assert get_task(task_id) is not None
    
    # Delete the task
    result = delete_task(task_id)
    assert result is True
    
    # Verify task no longer exists
    assert get_task(task_id) is None

def test_delete_task_nonexistent():
    """Test delete_task function with non-existent task"""
    # Try to delete a task that doesn't exist
    result = delete_task(999)
    assert result is False

def test_delete_task_from_multiple():
    """Test deleting one task from multiple tasks"""
    # Add multiple tasks
    task1 = add_task("Task 1", "Description 1")
    task2 = add_task("Task 2", "Description 2")
    task3 = add_task("Task 3", "Description 3")
    
    # Verify all tasks exist
    assert len(get_all_tasks()) == 3
    
    # Delete the middle task
    result = delete_task(task2.id)
    assert result is True
    
    # Verify only 2 tasks remain
    remaining_tasks = get_all_tasks()
    assert len(remaining_tasks) == 2
    
    # Verify the correct tasks remain
    task_ids = [task.id for task in remaining_tasks]
    assert task1.id in task_ids
    assert task3.id in task_ids
    assert task2.id not in task_ids

def test_delete_task_empty_database():
    """Test delete_task function when database is empty"""
    # Ensure database is empty
    assert len(get_all_tasks()) == 0
    
    # Try to delete a task
    result = delete_task(1)
    assert result is False

def test_delete_task_multiple_times():
    """Test deleting the same task multiple times"""
    # Add a task
    task = add_task("Test Task", "Test Description")
    task_id = task.id
    
    # Delete the task first time
    result = delete_task(task_id)
    assert result is True
    
    # Try to delete the same task again
    result = delete_task(task_id)
    assert result is False