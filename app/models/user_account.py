from sqlmodel import SQLModel, Field

class UserAccount(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password_hash: str