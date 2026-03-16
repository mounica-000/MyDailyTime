from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, auth_utils
from datetime import datetime, timedelta

# --- USER CRUD ---

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd = auth_utils.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# --- TASK CRUD ---

def get_tasks(db: Session, user_id: int, label: str = None, skip: int = 0, limit: int = 100):
    # Always filter by user_id first for security
    query = db.query(models.Task).filter(models.Task.owner_id == user_id)
    if label:
        query = query.filter(models.Task.label == label)
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    # Add owner_id here so the task is linked to the logged-in user
    db_task = models.Task(
        name=task.name,
        label=task.label,
        duration_minutes=task.duration_minutes,
        owner_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# --- ANALYTICS CRUD ---

def get_task_summary(db: Session, user_id: int, period: str = "all"):
    query = db.query(models.Task).filter(models.Task.owner_id == user_id)
    
    # Define time boundaries
    now = datetime.utcnow()
    
    if period == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Task.created_at >= start_date)
    elif period == "7days":
        start_date = now - timedelta(days=7)
        query = query.filter(models.Task.created_at >= start_date)
    
    # 1. Calculate total minutes for the selected period
    # We use .with_entities to just get the sum instead of the whole query
    total_minutes_res = query.with_entities(func.sum(models.Task.duration_minutes)).scalar()
    total_user_minutes = total_minutes_res or 0

    if total_user_minutes == 0:
        return []

    # 2. Group by label for that specific time period
    results = query.with_entities(
        models.Task.label,
        func.sum(models.Task.duration_minutes).label("total_minutes")
    ).group_by(models.Task.label).all()

    # 3. Format result
    summary = []
    for row in results:
        summary.append({
            "label": row.label,
            "total_minutes": row.total_minutes,
            "percentage": round((row.total_minutes / total_user_minutes) * 100, 2)
        })
    return summary