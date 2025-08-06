#!/usr/bin/env python3
"""
Simple test runner to verify the task description validation implementation
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    try:
        from src.models import Task, TaskStatus, TaskCreateRequest
        from src.main import app
        from src.utils import add_task, get_task, get_all_tasks
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_model_validation():
    """Test the TaskCreateRequest validation directly"""
    try:
        from src.models import TaskCreateRequest
        from pydantic import ValidationError
        
        # Test valid description
        valid_task = TaskCreateRequest(title="Test", description="A" * 150)
        print(f"✓ Valid description (150 chars): {len(valid_task.description)} characters")
        
        # Test invalid description
        try:
            invalid_task = TaskCreateRequest(title="Test", description="A" * 151)
            print("✗ Invalid description was accepted (should have failed)")
            return False
        except ValidationError as e:
            print(f"✓ Invalid description rejected: {e}")
            return True
            
    except Exception as e:
        print(f"✗ Model validation test failed: {e}")
        return False

def test_api_endpoint():
    """Test the API endpoint with FastAPI TestClient"""
    try:
        from fastapi.testclient import TestClient
        from src.main import app
        
        client = TestClient(app)
        
        # Test valid request
        valid_response = client.post("/tasks", json={
            "title": "Test Task",
            "description": "Valid description under 150 characters"
        })
        
        if valid_response.status_code == 200:
            print("✓ Valid task creation successful")
        else:
            print(f"✗ Valid task creation failed: {valid_response.status_code}")
            return False
        
        # Test invalid request
        invalid_response = client.post("/tasks", json={
            "title": "Test Task",
            "description": "A" * 151  # 151 characters
        })
        
        if invalid_response.status_code == 422:  # FastAPI returns 422 for validation errors
            print("✓ Invalid task creation properly rejected (422)")
            print(f"  Error details: {invalid_response.json()}")
            return True
        else:
            print(f"✗ Invalid task creation not properly rejected: {invalid_response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ API endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Task Description Validation Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Model Validation Tests", test_model_validation),
        ("API Endpoint Tests", test_api_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The implementation is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)