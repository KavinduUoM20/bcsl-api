from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .image import ImageRead
from .social_link import SocialLinkRead
from .external_link import ExternalLinkRead


class MemberBase(BaseModel):
    name: str
    slug: str
    user_name: str
    wallet_key: str
    bio: Optional[str]
    following: Optional[str]
    followers: Optional[str]
    joined_at: str


class MemberRead(MemberBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    avatar: Optional[ImageRead]
    cover_image: Optional[ImageRead]
    socials: List[SocialLinkRead]
    links: List[ExternalLinkRead]

    class Config:
        orm_mode = True