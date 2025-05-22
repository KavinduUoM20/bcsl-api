from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the async engine
engine = create_async_engine(settings.DATABASE_URI, echo=True)

# Create async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get DB session in routes/services
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session