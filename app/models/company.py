import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg

class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True))
    industry: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    website: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    email: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    phone: Optional[str] = Field(sa_column=Column(pg.VARCHAR(50), nullable=True))
    address: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    description: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Example relationship to events, if you want to add:
    # events: List["Event"] = Relationship(
    #     back_populates="organizing_company",
    #     sa_relationship_kwargs={"lazy": "selectin"}
    # )

    def __repr__(self):
        return f"<Company {self.name}>"