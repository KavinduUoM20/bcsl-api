from uuid import UUID
from pydantic import BaseModel


class FollowerRead(BaseModel):
    id: UUID
    follower_id: UUID
    followed_id: UUID

    model_config = {
        "from_attributes": True
    }
