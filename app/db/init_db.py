from sqlmodel import SQLModel
from db.session import engine

# Import all your models here to ensure they are registered in metadata
from models.member import Member
from models.image import Image
from models.social_link import SocialLink
from models.external_link import ExternalLink
from models.follower import Follower

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
