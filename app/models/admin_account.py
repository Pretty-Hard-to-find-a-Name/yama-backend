from sqlmodel import SQLModel, Field

class AdminAccount(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    license: str
    email_admin: str
    password_admin: str
