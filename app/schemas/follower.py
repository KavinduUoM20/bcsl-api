from uuid import UUID
from pydantic import BaseModel


class FollowerRead(BaseModel):
    id: UUID
    follower_id: UUID
    followed_id: UUID

    class Config:
        orm_mode = True
