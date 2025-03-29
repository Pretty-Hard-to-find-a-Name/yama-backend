from sqlmodel import SQLModel, Field

class SessionData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    session1: str | None = None
    session2: str | None = None
    session3: str | None = None