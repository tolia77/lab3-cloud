import json
from typing import Optional, Any
from redis import asyncio as aioredis
from app.settings import settings

redis = aioredis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True
)

async def get_cache(key: str) -> Optional[Any]:
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cache(key: str, data: Any, ttl: int = settings.REDIS_TTL):
    await redis.set(key, json.dumps(data), ex=ttl)

async def clear_cache(pattern: str = "*"):
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)