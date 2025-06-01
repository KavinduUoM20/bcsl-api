from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse, parse_qs

from app.core.config import settings

# Parse the DATABASE_URI to extract SSL mode
url = urlparse(str(settings.DATABASE_URI))
query_params = parse_qs(url.query)
ssl_required = 'sslmode' in query_params and query_params['sslmode'][0] == 'require'

# Create the async engine with SSL configuration if needed
engine = create_async_engine(
    str(settings.DATABASE_URI).split('?')[0],  # Base URL without query parameters
    echo=False,
    future=True,
    connect_args={"ssl": ssl_required} if ssl_required else {}
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)

# Dependency to get DB session in routes/services
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session