from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Member(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    slug: str
    user_name: str
    wallet_key: str
    bio: Optional[str] = None
    following: Optional[str] = None
    followers: Optional[str] = None
    joined_at: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    avatar_id: Optional[UUID] = Field(default=None, foreign_key="image.id")
    cover_image_id: Optional[UUID] = Field(default=None, foreign_key="image.id")

    avatar: Optional["Image"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    cover_image: Optional["Image"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})

    socials: list["SocialLink"] = Relationship(back_populates="member")
    links: list["ExternalLink"] = Relationship(back_populates="member")
    followers_list: list["Follower"] = Relationship(back_populates="followed")
