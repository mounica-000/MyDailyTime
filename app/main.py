from fastapi import FastAPI
from routers import tasks
from database.db_setup import Base, engine
from database import models

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")

app = FastAPI(
    title="MyDailyTime",
    description="A productivity tracking API that helps you monitor and analyze how you spend your time each day.",
    version="0.1.0"
)

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to MyDailyTime API!"}