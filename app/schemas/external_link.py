from uuid import UUID
from pydantic import BaseModel


class ExternalLinkRead(BaseModel):
    id: UUID
    title: str
    link: str

    class Config:
        orm_mode = True