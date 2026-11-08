from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    role_id: int
    facility_id: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role_id: int
    facility_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None
    facility_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
