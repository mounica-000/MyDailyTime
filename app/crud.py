# CRUD logic

from sqlalchemy.orm import Session
from . import models, schemas

# This handles "GET /tasks"
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

# This handles "POST /tasks"
def create_task(db: Session, task: schemas.TaskCreate):
    # Convert Pydantic object to SQLAlchemy model
    db_task = models.Task(
        name=task.name,
        label=task.label,
        duration_minutes=task.duration_minutes
    )
    # Add to session and commit to save to file
    db.add(db_task)
    db.commit()
    # Refresh to get the generated ID back from the DB
    db.refresh(db_task)
    return db_task