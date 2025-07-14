import pytest
from pydantic import ValidationError
from todo_list_app.src.models import Task

def test_task_description_length():
    # Test with valid description length
    task = Task(id=1, title="Test Task", description="A" * 150)
    assert task.description == "A" * 150

    # Test with invalid description length
    with pytest.raises(ValidationError):
        Task(id=2, title="Test Task", description="A" * 151)
