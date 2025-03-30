from app.models.license_info import LicenseInfo
from app.models.admin_account import AdminAccount
from app.models.user_account import UserAccount
from app.db.session import get_session
from datetime import datetime, timedelta
import hashlib
import secrets

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def seed():
    with get_session() as session:
        license_key = secrets.token_hex(21)  # 42 chars
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=7)

        license_info = LicenseInfo(
            license=license_key,
            account_max=5,
            account_used=2,
            start_date=start_date,
            end_date=end_date
        )
        session.add(license_info)

        admin = AdminAccount(
            license=license_key,
            email_admin="admin@example.com",
            password_admin=hash_password("admin")
        )
        session.add(admin)

        user = UserAccount(
            email="user@example.com",
            password=hash_password("user")
        )
        session.add(user)

        session.commit()
        print("Database seeded with admin and user accounts.")

if __name__ == "__main__":
    seed()