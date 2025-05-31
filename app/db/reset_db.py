import asyncio
from app.db.session import engine
from sqlmodel import SQLModel

async def reset_db():
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(SQLModel.metadata.drop_all)
        # Recreate all tables
        await conn.run_sync(SQLModel.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(reset_db()) 