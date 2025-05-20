from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class Follower(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    follower_id: UUID = Field(foreign_key="member.id")
    followed_id: UUID = Field(foreign_key="member.id")

    follower: "Member" = Relationship(sa_relationship_kwargs={"lazy": "joined"},
                                       sa_relationship="foreign(follower_id)")
    followed: "Member" = Relationship(back_populates="followers_list",
                                       sa_relationship="foreign(followed_id)")
