from uuid import UUID
from pydantic import BaseModel


class ImageRead(BaseModel):
    id: UUID
    thumbnail: str
    original: str

    class Config:
        orm_mode = True