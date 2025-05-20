from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class Image(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    thumbnail: str
    original: str