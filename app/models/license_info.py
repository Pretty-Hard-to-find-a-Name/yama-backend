from sqlmodel import SQLModel, Field

class LicenseInfo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    license: str
    account_max: int
    account_used: int