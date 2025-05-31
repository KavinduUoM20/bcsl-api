import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg

class User(SQLModel, table=True):
    __tablename__ = "users"

    # Primary Key
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )

    # Basic Information
    email: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True))
    phone: Optional[str] = Field(sa_column=Column(pg.VARCHAR(50), nullable=True))
    password_hash: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    
    # Role and status
    role: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False, default="member"))
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=True))
    
    # Verification statuses
    email_verified: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    phone_verified: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    
    # 2FA settings
    two_factor_enabled: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    two_factor_method: Optional[str] = Field(sa_column=Column(pg.VARCHAR(20), nullable=True))  # 'email' or 'sms'
    
    # Timestamps
    last_login: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Relationship with Member
    member_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("members.id"), unique=True, nullable=False)
    )
    member: "Member" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "joined"}
    )

    def __repr__(self):
        return f"<User {self.email}>"
