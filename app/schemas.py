from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum

# --- User Schemas ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True

# --- Task Schemas ---

class TaskLabel(str, Enum):
    STUDY = "study"
    WORK = "work"
    MEAL = "meal"
    HEALTH = "health"
    CAREER = "career"
    SLEEP = "sleep"
    BREAK = "break"
    OTHER = "other"

class TaskBase(BaseModel):
    name: str
    label: TaskLabel = TaskLabel.OTHER # Using constrained set of labels for now
    duration_minutes: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True