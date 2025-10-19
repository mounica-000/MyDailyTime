from fastapi import APIRouter
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Temporary list (connect to a DB later)
tasks = []

@router.get("/")
def get_tasks():
    return {"tasks": tasks}

@router.post("/")
def add_task(task: str):
    tasks.append(task)
    return {"message": "Task added successfully!", "tasks": tasks}

@router.delete("/{task_name}")
def delete_task(task_name: str):
    if task_name in tasks:
        tasks.remove(task_name)
        return {"message": f"Task '{task_name}' deleted successfully!"}
    return {"error": f"Task '{task_name}' not found."}