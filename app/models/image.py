from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg


class Image(SQLModel, table=True):
    __tablename__ = "images"

    id: UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    )
    thumbnail: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    original: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))