from uuid import UUID
from pydantic import BaseModel


class SocialLinkRead(BaseModel):
    id: UUID
    title: str
    link: str
    icon: str

    class Config:
        orm_mode = True