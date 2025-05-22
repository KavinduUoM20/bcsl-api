# Import all your models here to ensure they are registered in metadata
# from app.models.member import Member
# from app.models.image import Image
# from app.models.social_link import SocialLink
# from app.models.external_link import ExternalLink
# from app.models.follower import Follower

from sqlmodel import SQLModel,text
from sqlalchemy.ext.asyncio import AsyncEngine,create_async_engine
from app.core.config import settings
from app.db.session import engine

async_engine = create_async_engine(
    url=settings.DATABASE_URI,
    echo=True
)

async def init_db() -> None:
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.create_all)
        statement = text("SELECT 'Hello World';")
        result = await conn.execute(statement)
        print(result.all())