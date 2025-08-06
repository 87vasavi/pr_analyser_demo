#!/usr/bin/env python3

# Simple test script to verify the validation works
import sys
import os

# Add the todo_list_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_list_app'))

try:
    from src.models import Task, TaskCreateRequest
    from pydantic import ValidationError
    
    print("Testing Task model validation...")
    
    # Test 1: Valid task with short description
    try:
        task1 = Task(id=1, title="Test", description="Short description")
        print("✓ Valid task created successfully")
    except ValidationError as e:
        print(f"✗ Unexpected validation error: {e}")
    
    # Test 2: Valid task with exactly 150 characters
    try:
        description_150 = "A" * 150
        task2 = Task(id=2, title="Test", description=description_150)
        print("✓ Task with 150-character description created successfully")
    except ValidationError as e:
        print(f"✗ Unexpected validation error: {e}")
    
    # Test 3: Invalid task with 151 characters (should fail)
    try:
        description_151 = "A" * 151
        task3 = Task(id=3, title="Test", description=description_151)
        print("✗ Task with 151-character description should have failed validation")
    except ValidationError as e:
        print(f"✓ Validation correctly rejected 151-character description: {e}")
    
    # Test 4: TaskCreateRequest validation
    try:
        request1 = TaskCreateRequest(title="Test", description="Valid description")
        print("✓ Valid TaskCreateRequest created successfully")
    except ValidationError as e:
        print(f"✗ Unexpected validation error: {e}")
    
    # Test 5: TaskCreateRequest with long description (should fail)
    try:
        description_200 = "A" * 200
        request2 = TaskCreateRequest(title="Test", description=description_200)
        print("✗ TaskCreateRequest with 200-character description should have failed validation")
    except ValidationError as e:
        print(f"✓ Validation correctly rejected 200-character description: {e}")
    
    print("\nAll validation tests completed!")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required packages are installed")
except Exception as e:
    print(f"Unexpected error: {e}")