from fastapi import APIRouter, HTTPException
from app.api.schemas import AdminAccountCreateRequest
from app.db.session import get_session
from app.models.admin_account import AdminAccount
from app.api.schemas import UserAccountCreateRequest
from app.models.user_account import UserAccount
from app.models.license_info import LicenseInfo
from app.api.schemas import UserLoginRequest
from app.models.session_data import SessionData
from app.models.user_account import UserAccount
from app.api.schemas import TextCorrectionRequest
from app.models.session_data import SessionData
from openai import OpenAI
from sqlmodel import select
from sqlmodel import Session
from datetime import datetime, timedelta
from dotenv import load_dotenv
import secrets
import hashlib
import os
load_dotenv()
router = APIRouter()

@router.post("/admin/register")
def create_admin_account(data: AdminAccountCreateRequest):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    license_key = secrets.token_hex(21)  # 42 characters

    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=7)

    with get_session() as session:
        # Create license info entry
        license_info = LicenseInfo(
            license=license_key,
            account_max=1,
            account_used=1,
            start_date=start_date,
            end_date=end_date
        )
        session.add(license_info)

        # Create admin license account
        admin = AdminAccount(
            email_admin=data.email,
            password_admin=hashed_password,
            license=license_key
        )
        session.add(admin)

        session.commit()

    return {"message": "Admin account created", "license": license_key}


@router.post("/user/register")
def create_user_account(data: UserAccountCreateRequest):
    with get_session() as session:
        admin = session.exec(
            select(AdminAccount).where(AdminAccount.email_admin == data.admin_email)
        ).first()

        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        license_info = session.exec(
            select(LicenseInfo).where(LicenseInfo.license == admin.license)
        ).first()

        if not license_info:
            raise HTTPException(status_code=404, detail="License not found")

        if license_info.account_used >= license_info.account_max:
            raise HTTPException(status_code=403, detail="License quota exceeded")

        hashed_password = hashlib.sha256(data.password.encode()).hexdigest()

        user = UserAccount(
            email=data.email,
            password=hashed_password
        )
        session.add(user)

        license_info.account_used += 1
        session.add(license_info)

        session.commit()

    return {"message": "User account created and linked to license"}


@router.post("/user/login")
def login_user(data: UserLoginRequest):
    with get_session() as session:
        user = session.exec(
            select(UserAccount).where(UserAccount.email == data.email)
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed_input_password = hashlib.sha256(data.password.encode()).hexdigest()
        if user.password != hashed_input_password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # bring the session ID
        existing_sessions = session.exec(
            select(SessionData)
            .where(SessionData.email == data.email)
            .order_by(SessionData.created_at.asc())
        ).all()

        if len(existing_sessions) < 3 or not existing_sessions:
            # add new session
            new_session = SessionData(email=data.email, uid=data.uid)
            session.add(new_session)
        else:
            # replace the oldest session
            oldest_session = existing_sessions[0]
            oldest_session.uid = data.uid
            oldest_session.created_at = datetime.utcnow()
            session.add(oldest_session)

        session.commit()

    return {"message": "User logged in", "session_id": data.uid}


@router.post("/corrector")
def correct_text(data: TextCorrectionRequest):
    with get_session() as session:
        session_exists = session.exec(
            select(SessionData).where(SessionData.uid == data.uid)
        ).first()

        if not session_exists:
            raise HTTPException(status_code=401, detail="Invalid session")

        # TODO: implement IA-based text correction
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



        response = client.responses.create(
            model="gpt-4o-mini-2024-07-18",
            instructions="Corrige ce texte en français sans ajouter de commentaire, d’explication ou d’introduction. Ne réponds que par le texte corrigé :",
            input=data.text,
        )
        corrected_text = response.output_text

    return {
        "corrected": corrected_text
    }