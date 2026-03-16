from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas, auth_utils
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyDailyTime")

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Dependency ---
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_utils.jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except auth_utils.JWTError:
        raise credentials_exception
        
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---

@app.get("/")
def root():
    return {"message": "API is live!"}

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not auth_utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_utils.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(
    label: Optional[schemas.TaskLabel] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # This single call handles filtering, pagination, AND ownership
    return crud.get_tasks(db, user_id=current_user.id, label=label, skip=skip, limit=limit)

@app.get("/analytics/summary", response_model=List[schemas.TaskSummary])
def get_analytics(
    period: str = "all", # Options: "all", "today", "7days"
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    if period not in ["all", "today", "7days"]:
        raise HTTPException(status_code=400, detail="Invalid period")
    return crud.get_task_summary(db, user_id=current_user.id, period=period)