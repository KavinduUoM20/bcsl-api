# Import all your models here to ensure they are registered in metadata
from app.models.company import Company
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.session import engine

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)