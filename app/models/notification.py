import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg

class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    # Primary Key
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )

    # Content
    title: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    message: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    link: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    
    # Status and Type
    type: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))  # 'info', 'warning', 'error', 'success'
    priority: str = Field(sa_column=Column(pg.VARCHAR(20), nullable=False, default="normal"))  # 'low', 'normal', 'high', 'urgent'
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, default=True))
    
    # Timestamps
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    expires_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True))

    def __repr__(self):
        return f"<Notification {self.title}>" 