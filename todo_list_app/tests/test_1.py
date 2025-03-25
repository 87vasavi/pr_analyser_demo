import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.utils import task_db, add_task

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Task Management API is running"}

def test_create_task():
    response = client.post("/tasks", json={"title": "Test Task", "description": "This is a test task"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "This is a test task"

def test_update_task():
    # First, create a task to update
    task = add_task("Initial Task", "Initial Description")
    task_id = task.id

    # Update the task
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated Description", "status": "completed"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["status"] == "completed"

def test_update_non_existent_task():
    response = client.put("/tasks/999", json={"title": "Non-existent Task", "description": "No Description", "status": "completed"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
