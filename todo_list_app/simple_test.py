#!/usr/bin/env python3
"""
Simple test to verify DELETE endpoint implementation
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic delete functionality"""
    print("Testing basic DELETE functionality...")
    
    # Test the utility function first
    print("\n1. Testing delete_task utility function...")
    try:
        from src.utils import add_task, delete_task, get_task, task_db, task_counter
        
        # Reset database
        task_db.clear()
        globals()['task_counter'] = 1
        
        # Add a task
        task = add_task("Test Task", "Test Description")
        task_id = task.id
        print(f"   Created task with ID: {task_id}")
        
        # Verify task exists
        retrieved_task = get_task(task_id)
        if retrieved_task:
            print(f"   ✓ Task exists: {retrieved_task.title}")
        else:
            print("   ✗ Task not found after creation")
            return False
        
        # Delete the task
        result = delete_task(task_id)
        if result:
            print("   ✓ delete_task returned True")
        else:
            print("   ✗ delete_task returned False")
            return False
        
        # Verify task is gone
        retrieved_task = get_task(task_id)
        if retrieved_task is None:
            print("   ✓ Task successfully deleted")
        else:
            print("   ✗ Task still exists after deletion")
            return False
            
        # Test deleting non-existent task
        result = delete_task(999)
        if not result:
            print("   ✓ delete_task correctly returned False for non-existent task")
        else:
            print("   ✗ delete_task incorrectly returned True for non-existent task")
            return False
            
    except Exception as e:
        print(f"   Error testing utility function: {e}")
        return False
    
    # Test the API endpoint
    print("\n2. Testing DELETE API endpoint...")
    try:
        from fastapi.testclient import TestClient
        from src.main import app
        
        client = TestClient(app)
        
        # Reset database
        task_db.clear()
        
        # Create a task via API
        response = client.post("/tasks", params={"title": "API Test Task", "description": "API Test Description"})
        if response.status_code == 200:
            task_data = response.json()
            task_id = task_data["id"]
            print(f"   Created task via API with ID: {task_id}")
            
            # Delete the task via API
            delete_response = client.delete(f"/tasks/{task_id}")
            if delete_response.status_code == 200:
                response_data = delete_response.json()
                print(f"   ✓ DELETE returned 200 OK: {response_data}")
                
                # Verify task is gone
                get_response = client.get(f"/tasks/{task_id}")
                if get_response.status_code == 404:
                    print("   ✓ Task correctly returns 404 after deletion")
                else:
                    print(f"   ✗ Task still accessible after deletion: {get_response.status_code}")
                    return False
            else:
                print(f"   ✗ DELETE returned unexpected status: {delete_response.status_code}")
                return False
        else:
            print(f"   ✗ Failed to create task via API: {response.status_code}")
            return False
        
        # Test deleting non-existent task via API
        delete_response = client.delete("/tasks/999")
        if delete_response.status_code == 404:
            response_data = delete_response.json()
            print(f"   ✓ Non-existent task correctly returns 404: {response_data}")
        else:
            print(f"   ✗ Non-existent task returned unexpected status: {delete_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   Error testing API endpoint: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Simple DELETE endpoint test")
    print("=" * 40)
    
    success = test_basic_functionality()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed! DELETE endpoint implementation is working correctly.")
    else:
        print("✗ Some tests failed. Please check the implementation.")