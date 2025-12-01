from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="MyDailyTime",
    description="A productivity tracking API that helps you monitor and analyze how you spend your time each day.",
    version="0.1.0"
)

# Task Model
class Task(BaseModel):
    name: str
    label: Optional[str] = None
    duration_minutes: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None

# In-memory DB for now
tasks: List[dict] = []

# POST endpoint for tasks
@app.post("/tasks")
def create_task(task: Task):
    new_task = task.dict()
    new_task["id"] = len(tasks) + 1   # simple ID generation for now
    tasks.append(new_task)
    return new_task

# GET endpoint (for testing)
@app.get("/tasks")
def list_tasks():
    return tasks

@app.get("/")
def root():
    return {"message": "Welcome to MyDailyTime API!"}