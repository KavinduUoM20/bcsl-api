from uuid import UUID
from pydantic import BaseModel


class ImageRead(BaseModel):
    id: UUID
    thumbnail: str
    original: str

    model_config = {
        "from_attributes": True
    }