from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds
    user_id: int
    role: str
    facility_id: Optional[int] = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    token: str


class UserSummary(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    facility_id: Optional[int] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    token: Token
    user: UserSummary


class PasswordResetRequest(BaseModel):
    email: EmailStr
