from sqlmodel import SQLModel
from app.models.license_user import LicenseUser
from app.models.session_data import SessionData
from app.models.user_account import UserAccount
from app.models.license_info import LicenseInfo
from app.db.session import engine

def init_db():
    SQLModel.metadata.create_all(engine)