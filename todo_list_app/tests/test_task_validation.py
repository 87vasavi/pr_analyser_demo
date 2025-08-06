import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestTaskDescriptionValidation:
    """Test cases for task description character limit validation"""
    
    def test_create_task_with_valid_description(self):
        """Test creating a task with a description under 150 characters"""
        task_data = {
            "title": "Test Task",
            "description": "This is a valid description that is under 150 characters long."
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == task_data["title"]
        assert response_data["description"] == task_data["description"]
        assert "id" in response_data
        assert response_data["status"] == "pending"
    
    def test_create_task_with_exactly_150_characters(self):
        """Test creating a task with exactly 150 characters in description"""
        # Create a description with exactly 150 characters
        description_150_chars = "A" * 150
        
        task_data = {
            "title": "Test Task",
            "description": description_150_chars
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["description"] == description_150_chars
        assert len(response_data["description"]) == 150
    
    def test_create_task_with_description_over_150_characters(self):
        """Test creating a task with description over 150 characters should fail"""
        # Create a description with 151 characters
        description_151_chars = "A" * 151
        
        task_data = {
            "title": "Test Task",
            "description": description_151_chars
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 400  # Custom handler returns 400 instead of 422
        response_data = response.json()
        assert "detail" in response_data
        # Check that the error message is clear about the 150 character limit
        assert "150 characters" in response_data["detail"]
    
    def test_create_task_with_very_long_description(self):
        """Test creating a task with a very long description (500+ characters)"""
        description_500_chars = "A" * 500
        
        task_data = {
            "title": "Test Task",
            "description": description_500_chars
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 400  # Custom handler returns 400
        response_data = response.json()
        assert "detail" in response_data
    
    def test_create_task_with_empty_description(self):
        """Test creating a task with empty description should work"""
        task_data = {
            "title": "Test Task",
            "description": ""
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["description"] == ""
    
    def test_create_task_without_description_field(self):
        """Test creating a task without description field should fail since it's required"""
        task_data = {
            "title": "Test Task"
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 400  # Custom handler returns 400
        response_data = response.json()
        assert "detail" in response_data
        # Check that the error mentions the missing description field
        error_detail = str(response_data["detail"])
        assert "description" in error_detail.lower() or "required" in error_detail.lower()
    
    def test_multiple_validation_errors(self):
        """Test that validation works correctly with multiple potential issues"""
        task_data = {
            "title": "",  # Empty title might also be invalid
            "description": "A" * 200  # Over 150 characters
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 400  # Custom handler returns 400
        response_data = response.json()
        assert "detail" in response_data
    
    def test_create_task_with_special_characters_in_description(self):
        """Test creating a task with special characters in description under 150 chars"""
        task_data = {
            "title": "Test Task",
            "description": "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>? and unicode: 🚀✨🎉 (under 150)"
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["description"] == task_data["description"]
    
    def test_create_task_with_unicode_characters_over_limit(self):
        """Test that unicode characters are counted correctly for the 150 char limit"""
        # Create description with unicode characters that exceeds 150 characters
        unicode_description = "🚀" * 151  # Each emoji counts as one character
        
        task_data = {
            "title": "Test Task",
            "description": unicode_description
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 400  # Custom handler returns 400
        response_data = response.json()
        assert "detail" in response_data