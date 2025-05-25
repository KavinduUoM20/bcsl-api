from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl


class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True 
    }


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class CompanyRead(CompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }
