from uuid import UUID
from pydantic import BaseModel, HttpUrl


class SocialLinkBase(BaseModel):
    title: str
    link: HttpUrl
    icon: str

    model_config = {
        "from_attributes": True
    }


class SocialLinkCreate(SocialLinkBase):
    pass


class SocialLinkRead(SocialLinkBase):
    id: UUID
    member_id: UUID

    model_config = {
        "from_attributes": True
    }