from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class SocialLink(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title: str
    link: str
    icon: str

    member_id: UUID = Field(foreign_key="member.id")
    member: "Member" = Relationship(back_populates="socials")
