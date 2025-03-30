from sqlmodel import SQLModel, Field
from datetime import datetime

class LicenseInfo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    license: str
    account_max: int
    account_used: int
    start_date: datetime = Field(default_factory=datetime.utcnow) # default to current time
    end_date: datetime | None = None