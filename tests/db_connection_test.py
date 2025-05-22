# tests/db_connection_test.py

import asyncpg
import asyncio

async def test_pg_connection():
    try:
        conn = await asyncpg.connect("postgresql://neondb_owner:npg_Bp50jNEAxnvo@ep-winter-bread-a5a3jymu-pooler.us-east-2.aws.neon.tech/bcsl_db?sslmode=require")
        print("Connected successfully")
        await conn.close()
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    asyncio.run(test_pg_connection())
