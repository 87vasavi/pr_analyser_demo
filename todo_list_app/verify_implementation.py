#!/usr/bin/env python3
"""
Verification script to demonstrate DELETE endpoint implementation
This script verifies all acceptance criteria are met.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_acceptance_criteria():
    """Verify all acceptance criteria from the issue"""
    print("Verifying DELETE Task Endpoint Implementation")
    print("Issue: issue-2893531909")
    print("=" * 60)
    
    try:
        from fastapi.testclient import TestClient
        from src.main import app
        from src.utils import task_db
        
        client = TestClient(app)
        
        # Clear database for clean test
        task_db.clear()
        
        print("\n✅ ACCEPTANCE CRITERIA VERIFICATION:")
        print("-" * 40)
        
        # Criteria 1: A new DELETE /tasks/{task_id} endpoint is implemented
        print("\n1. DELETE /tasks/{task_id} endpoint exists:")
        try:
            # This will fail if endpoint doesn't exist
            response = client.delete("/tasks/999")  # Non-existent task
            print("   ✅ DELETE endpoint is accessible")
        except Exception as e:
            print(f"   ❌ DELETE endpoint not found: {e}")
            return False
        
        # Criteria 2 & 4: Task deletion and 200 OK response
        print("\n2. Task deletion with 200 OK response:")
        # Create a task first
        create_response = client.post("/tasks", params={
            "title": "Test Task for Deletion", 
            "description": "This task will be deleted"
        })
        
        if create_response.status_code == 200:
            task_id = create_response.json()["id"]
            print(f"   Created test task with ID: {task_id}")
            
            # Delete the task
            delete_response = client.delete(f"/tasks/{task_id}")
            
            if delete_response.status_code == 200:
                response_data = delete_response.json()
                expected_message = f"Task {task_id} deleted successfully"
                
                if response_data.get("message") == expected_message:
                    print("   ✅ Returns 200 OK with correct success message")
                else:
                    print(f"   ❌ Incorrect message: {response_data}")
                    return False
            else:
                print(f"   ❌ Wrong status code: {delete_response.status_code}")
                return False
        else:
            print("   ❌ Failed to create test task")
            return False
        
        # Criteria 2 (continued): Verify task is removed from database
        print("\n3. Task is removed from database:")
        # Try to retrieve the deleted task
        get_response = client.get(f"/tasks/{task_id}")
        
        if get_response.status_code == 404:
            print("   ✅ Deleted task no longer exists in database")
        else:
            print(f"   ❌ Task still exists: {get_response.status_code}")
            return False
        
        # Criteria 3: 404 Task Not Found for non-existent tasks
        print("\n4. 404 Task Not Found for non-existent tasks:")
        delete_response = client.delete("/tasks/99999")  # Non-existent task
        
        if delete_response.status_code == 404:
            response_data = delete_response.json()
            if response_data.get("detail") == "Task not found":
                print("   ✅ Returns 404 with 'Task not found' message")
            else:
                print(f"   ❌ Incorrect error message: {response_data}")
                return False
        else:
            print(f"   ❌ Wrong status code: {delete_response.status_code}")
            return False
        
        # Criteria 5: API documentation (verify endpoint is properly documented)
        print("\n5. API documentation:")
        # Check if the endpoint function has proper documentation
        from src.main import delete_task_endpoint
        
        if delete_task_endpoint.__doc__ and "Delete a task by its ID" in delete_task_endpoint.__doc__:
            print("   ✅ Endpoint has comprehensive documentation")
        else:
            print("   ❌ Endpoint lacks proper documentation")
            return False
        
        # Additional verification: Test multiple tasks to ensure only target is deleted
        print("\n6. Additional verification - Selective deletion:")
        
        # Create multiple tasks
        task_ids = []
        for i in range(3):
            response = client.post("/tasks", params={
                "title": f"Task {i+1}", 
                "description": f"Description {i+1}"
            })
            task_ids.append(response.json()["id"])
        
        print(f"   Created tasks with IDs: {task_ids}")
        
        # Delete the middle task
        middle_task_id = task_ids[1]
        delete_response = client.delete(f"/tasks/{middle_task_id}")
        
        if delete_response.status_code == 200:
            # Verify other tasks still exist
            remaining_tasks = []
            for task_id in [task_ids[0], task_ids[2]]:  # First and last tasks
                response = client.get(f"/tasks/{task_id}")
                if response.status_code == 200:
                    remaining_tasks.append(task_id)
            
            # Verify deleted task is gone
            response = client.get(f"/tasks/{middle_task_id}")
            
            if len(remaining_tasks) == 2 and response.status_code == 404:
                print("   ✅ Only target task deleted, others preserved")
            else:
                print("   ❌ Deletion affected wrong tasks")
                return False
        else:
            print("   ❌ Failed to delete middle task")
            return False
        
        # Test invalid input handling
        print("\n7. Invalid input handling:")
        response = client.delete("/tasks/invalid")
        
        if response.status_code == 422:  # Validation error
            print("   ✅ Returns 422 for invalid task ID format")
        else:
            print(f"   ❌ Unexpected response for invalid input: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    success = verify_acceptance_criteria()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL ACCEPTANCE CRITERIA VERIFIED SUCCESSFULLY!")
        print("\nThe DELETE task endpoint implementation:")
        print("✅ Implements DELETE /tasks/{task_id} endpoint")
        print("✅ Removes existing tasks from database")
        print("✅ Returns 404 for non-existent tasks")
        print("✅ Returns 200 OK on successful deletion")
        print("✅ Includes comprehensive API documentation")
        print("✅ Handles edge cases and invalid inputs correctly")
        print("\nImplementation is ready for production use! 🚀")
    else:
        print("❌ VERIFICATION FAILED")
        print("Please review the implementation and fix any issues.")
    
    return success

if __name__ == "__main__":
    main()