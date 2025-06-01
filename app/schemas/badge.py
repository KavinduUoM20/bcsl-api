from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BadgeBase(BaseModel):
    name: str
    description: str
    icon: str
    is_active: bool = True
    valid_from: datetime
    valid_until: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class BadgeRead(BadgeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class MemberBadgeBase(BaseModel):
    badge_id: UUID
    member_id: UUID
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }


class MemberBadgeCreate(MemberBadgeBase):
    pass


class MemberBadgeUpdate(BaseModel):
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


class MemberBadgeRead(MemberBadgeBase):
    id: UUID
    issued_at: datetime
    issued_by_id: UUID 