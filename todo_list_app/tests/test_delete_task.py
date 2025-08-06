import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.utils import task_db, task_counter

client = TestClient(app)

def setup_function():
    """Reset the task database before each test"""
    global task_counter
    task_db.clear()
    task_counter = 1

def test_delete_existing_task():
    """Test successful deletion of an existing task"""
    # First, create a task
    response = client.post("/tasks", params={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["id"]
    
    # Verify task exists
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Task {task_id} deleted successfully"}
    
    # Verify task no longer exists
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_nonexistent_task():
    """Test deletion of a task that doesn't exist"""
    # Try to delete a task that doesn't exist
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task_removes_from_database():
    """Test that deletion actually removes the task from the database"""
    # Create multiple tasks
    response1 = client.post("/tasks", params={"title": "Task 1", "description": "Description 1"})
    response2 = client.post("/tasks", params={"title": "Task 2", "description": "Description 2"})
    response3 = client.post("/tasks", params={"title": "Task 3", "description": "Description 3"})
    
    task1_id = response1.json()["id"]
    task2_id = response2.json()["id"]
    task3_id = response3.json()["id"]
    
    # Verify all tasks exist
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
    
    # Delete the middle task
    response = client.delete(f"/tasks/{task2_id}")
    assert response.status_code == 200
    
    # Verify only 2 tasks remain
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    
    # Verify the correct tasks remain
    task_ids = [task["id"] for task in tasks]
    assert task1_id in task_ids
    assert task3_id in task_ids
    assert task2_id not in task_ids

def test_delete_task_with_invalid_id_type():
    """Test deletion with invalid task ID type"""
    # Try to delete with a string ID (should be handled by FastAPI validation)
    response = client.delete("/tasks/invalid")
    assert response.status_code == 422  # Unprocessable Entity

def test_delete_already_deleted_task():
    """Test attempting to delete a task that was already deleted"""
    # Create a task
    response = client.post("/tasks", params={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Try to delete the same task again
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}