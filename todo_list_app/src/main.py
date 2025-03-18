from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(None, max_length=150)
    status: TaskStatus = TaskStatus.pending
    due_date: Optional[date] = None  # ➕ Added due_date field

    subtasks: List["Subtask"] = Relationship(back_populates="task")

class Subtask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    title: str
    completed: bool = False

    task: Optional[Task] = Relationship(back_populates="subtasks")
