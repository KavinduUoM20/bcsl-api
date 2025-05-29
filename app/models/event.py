import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column,ForeignKey
import sqlalchemy.dialects.postgresql as pg


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )
    
    title: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    description: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    location: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    start_time: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    end_time: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    cover_image_url: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    
    is_virtual: bool = Field(default=False, sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    registration_link: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    capacity: Optional[int] = Field(sa_column=Column(pg.INTEGER, nullable=True))
    
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Foreign key to company
    company_id: uuid.UUID = Field(sa_column=Column(
        pg.UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False
    )
    )

    # Back relationship to company
    organizing_company: Optional["Company"] = Relationship(
        back_populates="events",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Event {self.title}>"
