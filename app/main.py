from fastapi import FastAPI
from app.db.session import engine
from app.models.base import SQLModel, init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Backend ready"}