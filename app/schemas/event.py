from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    cover_image_url: Optional[HttpUrl] = None
    is_virtual: bool = False
    registration_link: Optional[HttpUrl] = None
    capacity: Optional[int] = None
    company_id: UUID

    model_config = {
        "from_attributes": True
    }


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    cover_image_url: Optional[HttpUrl] = None
    is_virtual: Optional[bool] = None
    registration_link: Optional[HttpUrl] = None
    capacity: Optional[int] = None
    company_id: Optional[UUID] = None

    model_config = {
        "from_attributes": True
    }


class EventRead(EventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
