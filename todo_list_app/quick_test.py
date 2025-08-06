#!/usr/bin/env python3
"""
Quick validation test for the task description character limit
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_validation():
    """Test basic Pydantic validation without FastAPI"""
    try:
        from src.models import TaskCreateRequest
        from pydantic import ValidationError
        
        print("Testing TaskCreateRequest validation...")
        
        # Test 1: Valid description (under 150 chars)
        try:
            valid_task = TaskCreateRequest(
                title="Test Task",
                description="This is a valid description under 150 characters."
            )
            print(f"✓ Valid task created: {len(valid_task.description)} characters")
        except Exception as e:
            print(f"✗ Valid task creation failed: {e}")
            return False
        
        # Test 2: Exactly 150 characters
        try:
            exact_150 = TaskCreateRequest(
                title="Test Task",
                description="A" * 150
            )
            print(f"✓ Task with exactly 150 characters created: {len(exact_150.description)} characters")
        except Exception as e:
            print(f"✗ Task with 150 characters failed: {e}")
            return False
        
        # Test 3: Over 150 characters (should fail)
        try:
            over_150 = TaskCreateRequest(
                title="Test Task", 
                description="A" * 151
            )
            print("✗ Task with 151 characters was accepted (should have failed)")
            return False
        except ValidationError as e:
            print(f"✓ Task with 151 characters properly rejected")
            print(f"  Validation error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
        
        # Test 4: Empty description
        try:
            empty_desc = TaskCreateRequest(
                title="Test Task",
                description=""
            )
            print("✓ Task with empty description created")
        except Exception as e:
            print(f"✗ Task with empty description failed: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_model_structure():
    """Test that the model has the expected structure"""
    try:
        from src.models import TaskCreateRequest, Task, TaskStatus
        
        print("\nTesting model structure...")
        
        # Check TaskCreateRequest fields
        task_req = TaskCreateRequest(title="Test", description="Test desc")
        assert hasattr(task_req, 'title')
        assert hasattr(task_req, 'description')
        print("✓ TaskCreateRequest has expected fields")
        
        # Check Task model
        from src.utils import add_task
        task = add_task("Test Title", "Test Description")
        assert hasattr(task, 'id')
        assert hasattr(task, 'title')
        assert hasattr(task, 'description')
        assert hasattr(task, 'status')
        print("✓ Task model has expected fields")
        
        return True
        
    except Exception as e:
        print(f"✗ Model structure test failed: {e}")
        return False

if __name__ == "__main__":
    print("Quick Validation Test")
    print("=" * 40)
    
    test1_result = test_basic_validation()
    test2_result = test_model_structure()
    
    print("\n" + "=" * 40)
    if test1_result and test2_result:
        print("🎉 All quick tests passed!")
        print("\nThe implementation appears to be working correctly:")
        print("- Task descriptions are limited to 150 characters")
        print("- Validation errors are properly raised for descriptions over 150 chars")
        print("- Empty descriptions are allowed")
        print("- Model structure is intact")
    else:
        print("❌ Some tests failed. Check the implementation.")
    
    sys.exit(0 if (test1_result and test2_result) else 1)