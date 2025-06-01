import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg


class Badge(SQLModel, table=True):
    __tablename__ = "badges"

    # Primary Key
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )

    # Badge Information
    name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    description: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    icon: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    
    # Status and Dates
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=True))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    valid_from: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    valid_until: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True))

    # Relationships
    members: List["MemberBadge"] = Relationship(
        back_populates="badge",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan"
        }
    )

    def __repr__(self):
        return f"<Badge {self.name}>"


class MemberBadge(SQLModel, table=True):
    """Association table for many-to-many relationship between Members and Badges"""
    __tablename__ = "member_badges"

    # Primary Key (composite)
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )

    # Foreign Keys
    member_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    )
    badge_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)
    )

    # Issue Information
    issued_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    issued_by_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    )
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=True))

    # Relationships
    member: "Member" = Relationship(back_populates="badges")
    badge: Badge = Relationship(back_populates="members")
    issued_by: "User" = Relationship() 