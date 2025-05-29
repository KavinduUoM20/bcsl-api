import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from .image import Image


class Member(SQLModel, table=True):
    __tablename__ = "members"

    # Primary Key
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )

    # Basic Information
    first_name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    last_name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    user_name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False, unique=True))
    email: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True))
    phone: Optional[str] = Field(sa_column=Column(pg.VARCHAR(50), nullable=True))
    
    # Profile Information
    bio: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    position: Optional[str] = Field(sa_column=Column(pg.VARCHAR(100), nullable=True))
    slug: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True))
    wallet_key: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True))
    
    # Status and Metrics
    following: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    followers: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    is_active: bool = Field(default=True, sa_column=Column(pg.BOOLEAN, nullable=False))
    
    # Timestamps
    joined_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Foreign Keys
    company_id: Optional[uuid.UUID] = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    )
    avatar_id: Optional[uuid.UUID] = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("images.id"), nullable=True)
    )
    cover_image_id: Optional[uuid.UUID] = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("images.id"), nullable=True)
    )

    # Relationships
    company: Optional["Company"] = Relationship(
        back_populates="members",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    avatar: Optional[Image] = Relationship(
        sa_relationship_kwargs={"lazy": "joined", "foreign_keys": "[Member.avatar_id]"}
    )
    cover_image: Optional[Image] = Relationship(
        sa_relationship_kwargs={"lazy": "joined", "foreign_keys": "[Member.cover_image_id]"}
    )
    socials: List["SocialLink"] = Relationship(
        back_populates="member",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )
    links: List["ExternalLink"] = Relationship(
        back_populates="member",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )
    followers_list: List["Follower"] = Relationship(
        back_populates="followed",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan",
            "foreign_keys": "[Follower.followed_id]"
        }
    )
    following_list: List["Follower"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan",
            "foreign_keys": "[Follower.follower_id]"
        }
    )

    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}>"
