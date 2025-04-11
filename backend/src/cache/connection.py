import asyncio
from typing import Dict

from redis.asyncio import Redis, from_url

from src.core.config import settings


class RedisCache:
    def __init__(self):
        # Support cache radis connections for several event loops
        self._connections: Dict[int, Redis] = {}

    async def get_connection(self) -> Redis:
        loop_id = id(asyncio.get_running_loop())
        if not self._connections.get(loop_id, None):
            self._connections[loop_id] = await from_url(settings.REDIS_CACHE)
        return self._connections[loop_id]


redis = RedisCache()
