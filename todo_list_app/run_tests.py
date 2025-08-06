#!/usr/bin/env python3
"""
Test runner script to verify the DELETE task endpoint implementation
"""
import sys
import os

# Add the current directory to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules and run them
if __name__ == "__main__":
    print("Testing DELETE task endpoint implementation...")
    print("=" * 50)
    
    # Test 1: Test the utility function
    print("\n1. Testing delete_task utility function...")
    try:
        from tests.test_utils import (
            setup_function, 
            test_delete_task_existing, 
            test_delete_task_nonexistent,
            test_delete_task_from_multiple,
            test_delete_task_empty_database,
            test_delete_task_multiple_times
        )
        
        # Run utility tests
        tests = [
            ("Delete existing task", test_delete_task_existing),
            ("Delete non-existent task", test_delete_task_nonexistent),
            ("Delete from multiple tasks", test_delete_task_from_multiple),
            ("Delete from empty database", test_delete_task_empty_database),
            ("Delete same task multiple times", test_delete_task_multiple_times)
        ]
        
        for test_name, test_func in tests:
            setup_function()  # Reset state
            try:
                test_func()
                print(f"   ✓ {test_name}")
            except Exception as e:
                print(f"   ✗ {test_name}: {e}")
                
    except Exception as e:
        print(f"   Error importing utility tests: {e}")
    
    # Test 2: Test the API endpoint
    print("\n2. Testing DELETE API endpoint...")
    try:
        from tests.test_delete_task import (
            setup_function as api_setup,
            test_delete_existing_task,
            test_delete_nonexistent_task,
            test_delete_task_removes_from_database,
            test_delete_task_with_invalid_id_type,
            test_delete_already_deleted_task
        )
        
        # Run API tests
        api_tests = [
            ("Delete existing task via API", test_delete_existing_task),
            ("Delete non-existent task via API", test_delete_nonexistent_task),
            ("Verify task removal from database", test_delete_task_removes_from_database),
            ("Invalid ID type handling", test_delete_task_with_invalid_id_type),
            ("Delete already deleted task", test_delete_already_deleted_task)
        ]
        
        for test_name, test_func in api_tests:
            api_setup()  # Reset state
            try:
                test_func()
                print(f"   ✓ {test_name}")
            except Exception as e:
                print(f"   ✗ {test_name}: {e}")
                
    except Exception as e:
        print(f"   Error importing API tests: {e}")
    
    print("\n" + "=" * 50)
    print("Test execution completed!")
    
    # Test 3: Manual verification of the endpoint
    print("\n3. Manual verification of DELETE endpoint...")
    try:
        from fastapi.testclient import TestClient
        from src.main import app
        from src.utils import task_db
        
        client = TestClient(app)
        
        # Clear database
        task_db.clear()
        
        # Create a task
        response = client.post("/tasks", params={"title": "Manual Test Task", "description": "Test Description"})
        if response.status_code == 200:
            task_id = response.json()["id"]
            print(f"   ✓ Created task with ID: {task_id}")
            
            # Delete the task
            delete_response = client.delete(f"/tasks/{task_id}")
            if delete_response.status_code == 200:
                print(f"   ✓ Successfully deleted task {task_id}")
                print(f"   ✓ Response: {delete_response.json()}")
                
                # Verify task is gone
                get_response = client.get(f"/tasks/{task_id}")
                if get_response.status_code == 404:
                    print("   ✓ Confirmed task no longer exists")
                else:
                    print("   ✗ Task still exists after deletion")
            else:
                print(f"   ✗ Failed to delete task: {delete_response.status_code}")
        else:
            print(f"   ✗ Failed to create test task: {response.status_code}")
            
        # Test deleting non-existent task
        delete_response = client.delete("/tasks/999")
        if delete_response.status_code == 404:
            print("   ✓ Correctly returned 404 for non-existent task")
        else:
            print(f"   ✗ Unexpected response for non-existent task: {delete_response.status_code}")
            
    except Exception as e:
        print(f"   Error in manual verification: {e}")
    
    print("\nAll tests completed!")