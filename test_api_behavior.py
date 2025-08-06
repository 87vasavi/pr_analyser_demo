#!/usr/bin/env python3

# Test script to verify API behavior
import sys
import os

# Add the todo_list_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_list_app'))

try:
    from fastapi.testclient import TestClient
    from src.main import app
    from src.utils import task_db, task_counter
    
    # Reset the database
    task_db.clear()
    task_counter = 1
    
    client = TestClient(app)
    
    print("Testing API behavior...")
    
    # Test 1: Valid task creation
    print("\n1. Testing valid task creation...")
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "This is a valid description"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Task creation with exactly 150 characters
    print("\n2. Testing task creation with exactly 150 characters...")
    description_150 = "A" * 150
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": description_150
    })
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Description length: {len(response.json()['description'])}")
    else:
        print(f"Response: {response.json()}")
    
    # Test 3: Task creation with 151 characters (should fail)
    print("\n3. Testing task creation with 151 characters (should fail)...")
    description_151 = "A" * 151
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": description_151
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Task creation with much longer description (should fail)
    print("\n4. Testing task creation with 200 characters (should fail)...")
    description_200 = "A" * 200
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": description_200
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 5: Task creation without description (should succeed)
    print("\n5. Testing task creation without description...")
    response = client.post("/tasks", json={
        "title": "Test Task Without Description"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 6: Task creation with missing title (should fail)
    print("\n6. Testing task creation with missing title (should fail)...")
    response = client.post("/tasks", json={
        "description": "Valid description"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\nAPI behavior testing completed!")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("This might be expected if FastAPI/TestClient is not available")
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()