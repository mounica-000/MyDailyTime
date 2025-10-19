from fastapi import FastAPI

app = FastAPI(
    title="MyDailyTime",
    description="A productivity tracking API that helps you monitor and analyze how you spend your time each day.",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to MyDailyTime API!"}