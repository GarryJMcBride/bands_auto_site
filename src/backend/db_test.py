import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Globals and Configurations
load_dotenv()  # Load environment variables from .env file

async def test():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    print("Connected successfully")
    await conn.close()

asyncio.run(test())