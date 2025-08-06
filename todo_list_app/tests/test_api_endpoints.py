import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.utils import task_db, task_counter

client = TestClient(app)

class TestTaskAPIEndpoints:
    """Test cases for Task Management API endpoints"""
    
    def setup_method(self):
        """Clear the task database before each test"""
        global task_db, task_counter
        task_db.clear()
        # Reset counter to 1 for consistent testing
        import src.utils
        src.utils.task_counter = 1
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "Task Management API is running"}
    
    def test_create_and_retrieve_task(self):
        """Test creating a task and then retrieving it"""
        # Create a task
        task_data = {
            "title": "Test Task",
            "description": "This is a test task description"
        }
        
        create_response = client.post("/tasks", json=task_data)
        assert create_response.status_code == 200
        
        created_task = create_response.json()
        task_id = created_task["id"]
        
        # Retrieve the task
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        
        retrieved_task = get_response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == task_data["title"]
        assert retrieved_task["description"] == task_data["description"]
        assert retrieved_task["status"] == "pending"
    
    def test_retrieve_nonexistent_task(self):
        """Test retrieving a task that doesn't exist"""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"
    
    def test_list_empty_tasks(self):
        """Test listing tasks when no tasks exist"""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_multiple_tasks(self):
        """Test listing multiple tasks"""
        # Create multiple tasks
        tasks_data = [
            {"title": "Task 1", "description": "Description 1"},
            {"title": "Task 2", "description": "Description 2"},
            {"title": "Task 3", "description": "Description 3"}
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            response = client.post("/tasks", json=task_data)
            assert response.status_code == 200
            created_tasks.append(response.json())
        
        # List all tasks
        list_response = client.get("/tasks")
        assert list_response.status_code == 200
        
        tasks_list = list_response.json()
        assert len(tasks_list) == 3
        
        # Verify all created tasks are in the list
        for i, task in enumerate(tasks_list):
            assert task["title"] == tasks_data[i]["title"]
            assert task["description"] == tasks_data[i]["description"]
            assert task["status"] == "pending"
    
    def test_task_id_increments(self):
        """Test that task IDs increment correctly"""
        task_data = {"title": "Test Task", "description": "Test description"}
        
        # Create first task
        response1 = client.post("/tasks", json=task_data)
        task1 = response1.json()
        
        # Create second task
        response2 = client.post("/tasks", json=task_data)
        task2 = response2.json()
        
        assert task2["id"] == task1["id"] + 1
    
    def test_create_task_with_minimal_data(self):
        """Test creating a task with minimal required data"""
        task_data = {
            "title": "Minimal Task",
            "description": ""
        }
        
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 200
        
        task = response.json()
        assert task["title"] == task_data["title"]
        assert task["description"] == task_data["description"]
        assert task["status"] == "pending"
        assert "id" in task
    
    def test_create_task_missing_title(self):
        """Test creating a task without a title should fail"""
        task_data = {
            "description": "Task without title"
        }
        
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 400  # Custom handler returns 400
        
        error_detail = response.json()["detail"]
        assert "title" in str(error_detail).lower() or "required" in str(error_detail).lower()
    
    def test_api_response_format(self):
        """Test that API responses have the correct format"""
        task_data = {
            "title": "Format Test Task",
            "description": "Testing response format"
        }
        
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 200
        
        task = response.json()
        
        # Check all required fields are present
        required_fields = ["id", "title", "description", "status"]
        for field in required_fields:
            assert field in task
        
        # Check field types
        assert isinstance(task["id"], int)
        assert isinstance(task["title"], str)
        assert isinstance(task["description"], (str, type(None)))
        assert isinstance(task["status"], str)
        assert task["status"] in ["pending", "in_progress", "completed"]