from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = Field(None, max_length=150)
    status: TaskStatus = TaskStatus.pending
