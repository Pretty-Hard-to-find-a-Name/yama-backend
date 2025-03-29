from sqlmodel import SQLModel, Field

class LicenseUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    license: str
    email: str