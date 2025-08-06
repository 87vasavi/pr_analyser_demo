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

def test_create_task_success():
    """Test successful task creation with valid description"""
    setup_function()
    
    task_data = {
        "title": "Test Task",
        "description": "This is a valid description under 150 characters"
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Task"
    assert response_data["description"] == "This is a valid description under 150 characters"
    assert response_data["id"] == 1
    assert response_data["status"] == "pending"

def test_create_task_success_no_description():
    """Test successful task creation without description"""
    setup_function()
    
    task_data = {
        "title": "Test Task Without Description"
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Task Without Description"
    assert response_data["description"] is None
    assert response_data["id"] == 1
    assert response_data["status"] == "pending"

def test_create_task_success_empty_description():
    """Test successful task creation with empty description"""
    setup_function()
    
    task_data = {
        "title": "Test Task",
        "description": ""
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Task"
    assert response_data["description"] == ""
    assert response_data["id"] == 1
    assert response_data["status"] == "pending"

def test_create_task_success_exactly_150_chars():
    """Test successful task creation with description exactly 150 characters"""
    setup_function()
    
    # Create a description that is exactly 150 characters
    description_150_chars = "A" * 150
    
    task_data = {
        "title": "Test Task",
        "description": description_150_chars
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Task"
    assert response_data["description"] == description_150_chars
    assert len(response_data["description"]) == 150

def test_create_task_fail_description_too_long():
    """Test task creation failure with description longer than 150 characters"""
    setup_function()
    
    # Create a description that is 151 characters (1 over the limit)
    description_151_chars = "A" * 151
    
    task_data = {
        "title": "Test Task",
        "description": description_151_chars
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 400  # Custom handler returns 400 for validation errors
    response_data = response.json()
    assert "detail" in response_data
    # Check that the error mentions the length constraint
    error_detail = response_data["detail"]
    assert "150 characters" in error_detail

def test_create_task_fail_description_much_too_long():
    """Test task creation failure with description much longer than 150 characters"""
    setup_function()
    
    # Create a description that is 300 characters (way over the limit)
    description_300_chars = "A" * 300
    
    task_data = {
        "title": "Test Task",
        "description": description_300_chars
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 400  # Custom handler returns 400 for validation errors
    response_data = response.json()
    assert "detail" in response_data
    # Check that the error mentions the length constraint
    error_detail = response_data["detail"]
    assert "150 characters" in error_detail

def test_create_task_fail_missing_title():
    """Test task creation failure when title is missing"""
    setup_function()
    
    task_data = {
        "description": "Valid description"
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 400  # Custom handler returns 400 for validation errors
    response_data = response.json()
    assert "detail" in response_data

def test_multiple_tasks_creation():
    """Test creating multiple tasks to ensure counter works correctly"""
    setup_function()
    
    # Create first task
    task_data_1 = {
        "title": "First Task",
        "description": "First task description"
    }
    response_1 = client.post("/tasks", json=task_data_1)
    assert response_1.status_code == 200
    assert response_1.json()["id"] == 1
    
    # Create second task
    task_data_2 = {
        "title": "Second Task",
        "description": "Second task description"
    }
    response_2 = client.post("/tasks", json=task_data_2)
    assert response_2.status_code == 200
    assert response_2.json()["id"] == 2