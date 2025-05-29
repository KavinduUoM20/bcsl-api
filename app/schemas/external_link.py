from uuid import UUID
from pydantic import BaseModel, HttpUrl


class ExternalLinkBase(BaseModel):
    title: str
    link: HttpUrl

    model_config = {
        "from_attributes": True
    }


class ExternalLinkCreate(ExternalLinkBase):
    pass


class ExternalLinkRead(ExternalLinkBase):
    id: UUID
    member_id: UUID

    model_config = {
        "from_attributes": True
    }