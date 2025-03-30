from fastapi import FastAPI
from app.db.session import engine
from app.models.base import SQLModel, init_db
from app.api.routes import router
import time
from sqlalchemy.exc import OperationalError

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(router)

@app.get("/")
def root():
    return {"message": "Backend ready"}