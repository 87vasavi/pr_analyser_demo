import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_task_with_valid_description():
    response = client.post("/tasks", params={"task":"new_task", "description": "A valid task description."})
    assert response.status_code == 200
    assert response.json()["description"] == "A valid task description."

def test_create_task_with_long_description():
    long_description = "x" * 151
    response = client.post("/tasks", params={"task":"new_task", "description": long_description})
    assert response.status_code == 400
    assert response.json()["detail"] == "Description cannot exceed 150 characters."
