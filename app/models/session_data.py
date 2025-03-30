from sqlmodel import SQLModel, Field
from datetime import datetime

class SessionData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    uid: str
    created_at: datetime = Field(default_factory=datetime.utcnow)