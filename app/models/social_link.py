from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg


class SocialLink(SQLModel, table=True):
    __tablename__ = "sociallinks"

    id: UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    )
    title: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    link: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    icon: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))

    member_id: UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    )
    member: "Member" = Relationship(
        back_populates="socials",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
