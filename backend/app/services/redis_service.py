import json
import redis.asyncio as redis
from typing import Optional, Any
from app.core.config import settings

class RedisService:
    _client: Optional[redis.Redis] = None

    @classmethod
    async def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return cls._client

    @classmethod
    async def get_cache(cls, key: str) -> Optional[dict]:
        client = await cls.get_client()
        data = await client.get(key)
        if data:
            return json.loads(data)
        return None

    @classmethod
    async def set_cache(cls, key: str, value: Any, expire: int = 3600):
        client = await cls.get_client()
        await client.set(key, json.dumps(value), ex=expire)

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None
