# Pydantic models (Data validation/API shapes)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    label: Optional[str] = None
    duration_minutes: int

class TaskCreate(TaskBase):
    pass # Data needed to create a task

class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Tells Pydantic to read data from SQLAlchemy objects