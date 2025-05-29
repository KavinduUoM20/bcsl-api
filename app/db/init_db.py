# Import all your models here to ensure they are registered in metadata
from app.models.company import Company
from app.models.event import Event
from app.models.member import Member
from app.models.image import Image
from app.models.social_link import SocialLink
from app.models.external_link import ExternalLink
from app.models.follower import Follower
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.session import engine

async def drop_db() -> None:
    """WARNING: This will drop all tables. Use only in development."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

async def init_db() -> None:
    """Initialize database tables if they don't exist."""
    async with engine.begin() as conn:
        # Create tables without dropping existing ones
        await conn.run_sync(SQLModel.metadata.create_all)