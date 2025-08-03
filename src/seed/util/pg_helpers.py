import os
import asyncpg
from typing import Optional

_pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(os.getenv("DB_URL"))
    return _pool

async def acquire_connection():
    pool = await get_pool()
    async with pool.acquire() as conn:
        yield conn
