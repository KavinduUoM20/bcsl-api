import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg


class Follower(SQLModel, table=True):
    __tablename__ = "followers"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )
    follower_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    )
    followed_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )

    # Relationships
    follower: "Member" = Relationship(
        back_populates="following_list",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[Follower.follower_id]"
        }
    )
    followed: "Member" = Relationship(
        back_populates="followers_list",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[Follower.followed_id]"
        }
    )
