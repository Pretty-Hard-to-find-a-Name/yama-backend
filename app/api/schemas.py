from pydantic import BaseModel, EmailStr, Field

class AdminAccountCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class UserAccountCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    admin_email: EmailStr

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    uid: str

class TextCorrectionRequest(BaseModel):
    uid: str
    text: str