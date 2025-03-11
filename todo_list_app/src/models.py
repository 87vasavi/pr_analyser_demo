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

class Subtask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    title: str
    completed: bool = False
    task: Task = Relationship(back_populates="subtasks")
