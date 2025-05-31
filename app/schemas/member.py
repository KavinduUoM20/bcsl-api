from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl

from .image import ImageRead
from .social_link import SocialLinkRead
from .external_link import ExternalLinkRead


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    phone: Optional[str] = None
    bio: Optional[str] = None
    position: Optional[str] = None
    slug: str
    wallet_key: str
    following: Optional[str] = None
    followers: Optional[str] = None
    company_id: Optional[UUID] = None
    is_active: bool = True
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }


class MemberCreate(MemberBase):
    avatar_id: Optional[UUID] = None
    cover_image_id: Optional[UUID] = None


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    position: Optional[str] = None
    slug: Optional[str] = None
    wallet_key: Optional[str] = None
    following: Optional[str] = None
    followers: Optional[str] = None
    company_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    avatar_id: Optional[UUID] = None
    cover_image_id: Optional[UUID] = None

    model_config = {
        "from_attributes": True
    }


class MemberRead(MemberBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    avatar: Optional[ImageRead] = None
    cover_image: Optional[ImageRead] = None
    socials: List[SocialLinkRead] = []
    links: List[ExternalLinkRead] = []

    model_config = {
        "from_attributes": True
    }


class MemberPublicRead(BaseModel):
    """
    Public member information schema - used for followers/following lists and public profile views.
    Only includes information that should be publicly visible.
    """
    id: UUID
    first_name: str
    last_name: str
    user_name: str
    slug: str
    bio: Optional[str] = None
    position: Optional[str] = None
    followers: Optional[str] = None
    following: Optional[str] = None
    is_active: bool = True
    avatar_id: Optional[UUID] = None
    cover_image_id: Optional[UUID] = None
    socials: Optional[List[SocialLinkRead]] = None
    links: Optional[List[ExternalLinkRead]] = None

    model_config = {
        "from_attributes": True
    }