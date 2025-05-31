from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True
    role: str = "member"  # default role

    model_config = {
        "from_attributes": True
    }

class UserCreate(UserBase):
    password: str
    # member_id will be set internally during registration

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
    email_verified: Optional[bool] = None
    phone_verified: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None
    two_factor_method: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class UserRead(UserBase):
    id: UUID
    member_id: UUID
    email_verified: bool
    phone_verified: bool
    two_factor_enabled: bool
    two_factor_method: Optional[str]
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

# Schema for authentication
class UserLogin(BaseModel):
    email: EmailStr
    password: str
