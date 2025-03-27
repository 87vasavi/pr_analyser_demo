import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_session
from models import Base, Task, Subtask

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_session dependency
def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

# Create the database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create a sample task for testing
    db = TestingSessionLocal()
    task = Task(title="Sample Task")
    db.add(task)
    db.commit()
    db.refresh(task)
    yield
    # Teardown: Drop all tables
    Base.metadata.drop_all(bind=engine)

def test_create_subtask_success():
    # Test creating a subtask successfully
    response = client.post("/tasks/1/subtasks/", json={"title": "Sample Subtask"})
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Subtask"
    assert response.json()["task_id"] == 1

def test_create_subtask_task_not_found():
    # Test creating a subtask for a non-existent task
    response = client.post("/tasks/999/subtasks/", json={"title": "Non-existent Task Subtask"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create_subtask_description_too_long():
    # Test creating a subtask with a description that exceeds 150 characters
    long_description = "x" * 151
    response = client.post("/tasks/1/subtasks/", json={"title": "Subtask with long description", "description": long_description})
    assert response.status_code == 400
    assert response.json()["detail"] == "Description cannot exceed 150 characters"

def test_complete_subtask_success():
    # First, create a subtask to complete
    response = client.post("/tasks/1/subtasks/", json={"title": "Subtask to Complete"})
    subtask_id = response.json()["id"]

    # Test marking the subtask as complete
    response = client.patch(f"/subtasks/{subtask_id}/complete/")
    assert response.status_code == 200
    assert response.json()["message"] == "Subtask marked as completed"

def test_complete_subtask_not_found():
    # Test completing a non-existent subtask
    response = client.patch("/subtasks/999/complete/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Subtask not found"

# Additional tests can be added here to cover more edge cases and scenarios
