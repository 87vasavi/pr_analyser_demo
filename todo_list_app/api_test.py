#!/usr/bin/env python3
"""
API Test for Task Description Validation
Tests the actual FastAPI endpoint behavior
"""

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_validation():
    """Test the API endpoint validation"""
    try:
        from fastapi.testclient import TestClient
        from src.main import app
        
        client = TestClient(app)
        
        print("Testing API endpoint validation...")
        
        # Test 1: Health check
        health_response = client.get("/")
        if health_response.status_code == 200:
            print("✓ Health check endpoint working")
        else:
            print(f"✗ Health check failed: {health_response.status_code}")
            return False
        
        # Test 2: Valid task creation (under 150 chars)
        valid_task = {
            "title": "Test Task",
            "description": "This is a valid description that is under the 150 character limit for testing purposes."
        }
        
        valid_response = client.post("/tasks", json=valid_task)
        if valid_response.status_code == 200:
            task_data = valid_response.json()
            print(f"✓ Valid task created successfully")
            print(f"  Task ID: {task_data.get('id')}")
            print(f"  Description length: {len(task_data.get('description', ''))}")
        else:
            print(f"✗ Valid task creation failed: {valid_response.status_code}")
            print(f"  Response: {valid_response.text}")
            return False
        
        # Test 3: Task with exactly 150 characters
        exact_150_task = {
            "title": "Exact 150 Test",
            "description": "A" * 150
        }
        
        exact_response = client.post("/tasks", json=exact_150_task)
        if exact_response.status_code == 200:
            print("✓ Task with exactly 150 characters created successfully")
        else:
            print(f"✗ Task with 150 characters failed: {exact_response.status_code}")
            return False
        
        # Test 4: Invalid task creation (over 150 chars)
        invalid_task = {
            "title": "Invalid Task",
            "description": "A" * 151  # 151 characters
        }
        
        invalid_response = client.post("/tasks", json=invalid_task)
        print(f"\nTesting invalid task (151 characters):")
        print(f"  Status Code: {invalid_response.status_code}")
        print(f"  Response: {json.dumps(invalid_response.json(), indent=2)}")
        
        if invalid_response.status_code == 400:  # Now expecting 400 due to custom handler
            error_data = invalid_response.json()
            if "detail" in error_data:
                print("✓ Invalid task properly rejected with error details")
                
                # Check if error mentions the 150 character limit
                error_str = str(error_data["detail"]).lower()
                if "150 characters" in error_str:
                    print("✓ Error message clearly mentions the 150 character limit")
                else:
                    print("⚠ Error message doesn't clearly mention the 150 character limit")
                    print(f"  Error details: {error_data['detail']}")
            else:
                print("⚠ Error response doesn't have 'detail' field")
        else:
            print(f"✗ Invalid task not properly rejected: {invalid_response.status_code}")
            return False
        
        # Test 5: Very long description (500+ chars)
        very_long_task = {
            "title": "Very Long Test",
            "description": "A" * 500
        }
        
        very_long_response = client.post("/tasks", json=very_long_task)
        if very_long_response.status_code == 400:  # Expecting 400
            print("✓ Very long description properly rejected")
        else:
            print(f"✗ Very long description not rejected: {very_long_response.status_code}")
            return False
        
        # Test 6: Empty description
        empty_desc_task = {
            "title": "Empty Description Test",
            "description": ""
        }
        
        empty_response = client.post("/tasks", json=empty_desc_task)
        if empty_response.status_code == 200:
            print("✓ Empty description accepted")
        else:
            print(f"✗ Empty description rejected: {empty_response.status_code}")
            return False
        
        # Test 7: Missing description field
        missing_desc_task = {
            "title": "Missing Description Test"
        }
        
        missing_response = client.post("/tasks", json=missing_desc_task)
        if missing_response.status_code in [400, 422]:
            print("✓ Missing description field properly rejected")
        else:
            print(f"✗ Missing description not rejected: {missing_response.status_code}")
            return False
        
        # Test 8: List tasks to verify storage works
        list_response = client.get("/tasks")
        if list_response.status_code == 200:
            tasks = list_response.json()
            print(f"✓ Task listing works, found {len(tasks)} tasks")
        else:
            print(f"✗ Task listing failed: {list_response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ API test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("API Validation Test")
    print("=" * 50)
    
    result = test_api_validation()
    
    print("\n" + "=" * 50)
    if result:
        print("🎉 API validation tests passed!")
        print("\nImplementation Summary:")
        print("- ✓ Task descriptions are validated for 150 character limit")
        print("- ✓ Valid tasks are created successfully")
        print("- ✓ Invalid tasks are rejected with appropriate errors")
        print("- ✓ Empty descriptions are allowed")
        print("- ✓ Missing description field is rejected")
        print("- ✓ Task storage and retrieval works correctly")
        print("\nNote: FastAPI returns 422 for validation errors (standard behavior)")
        print("If 400 status code is strictly required, custom error handling can be added.")
    else:
        print("❌ API validation tests failed!")
    
    return result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)