import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_delete_task_success():
    # Assuming task with ID 1 exists
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Task 1 deleted"}

def test_delete_task_not_found():
    # Assuming task with ID 999 does not exist
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
