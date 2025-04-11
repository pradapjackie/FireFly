import asyncio
from contextlib import asynccontextmanager
from enum import StrEnum
from typing import Any, AsyncGenerator, AsyncIterator, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import WebSocket
from pydantic import BaseModel
from redis.asyncio import Redis

from src.cache.connection import redis
from src.cache.converter import PydanticRedisConverter

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


async def redis_key_exist_with_wait(
    conn: Redis, key: str, wait_seconds: float = 5.0, poll_timeout: float = 0.5
) -> bool:
    try:
        async with asyncio.timeout(wait_seconds):
            while True:
                if await conn.exists(key):
                    return True
                else:
                    await asyncio.sleep(poll_timeout)
    except TimeoutError:
        return False


async def delete_key_with_delay(conn: Redis, key: str, delay_seconds: float = 60):
    await asyncio.sleep(delay_seconds)
    await conn.delete(key)


class CacheBase(Generic[CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model_class: Optional[Type[CreateSchemaType]] = None):
        self.converter = PydanticRedisConverter(model_class)

    @asynccontextmanager
    async def _get_redis(self) -> AsyncGenerator[Redis, None]:
        yield await redis.get_connection()

    async def _create_key(self, key: str, value: Union[str, bytes]):
        async with self._get_redis() as conn:
            await conn.set(key, value)

    async def _get_key(self, key: str) -> bytes:
        async with self._get_redis() as conn:
            return await conn.get(key)

    async def _get_list_of_keys_from_dict(self, key: str) -> List[str]:
        async with self._get_redis() as conn:
            return await conn.hkeys(key)

    async def _delete_key(self, key: str):
        async with self._get_redis() as conn:
            await conn.delete(key)

    async def _save_dict(self, key: str, data: Dict[str, Union[str, int, float]]):
        async with self._get_redis() as conn:
            await conn.hset(key, mapping=data)

    async def _get_dict(self, key: str) -> dict:
        async with self._get_redis() as conn:
            return await conn.hgetall(key)

    async def _get_decoded_dict(self, key: str) -> dict:
        async with self._get_redis() as conn:
            raw_dict = await conn.hgetall(key)
            return {k.decode("UTF-8"): v.decode("UTF-8") for k, v in raw_dict.items()}

    async def _get_value_from_model(self, key: str, sub_key: str) -> Any:
        async with self._get_redis() as conn:
            result = await conn.hmget(key, [sub_key])
            assert len(result) == 1 and result[0] is not None, f"Incorrect data found for {key}:{sub_key}: {result}"
            return self.converter.decode_value(result[0])

    async def _get_values_from_dict(self, key: str, sub_keys: List[str]) -> List[str]:
        async with self._get_redis() as conn:
            result = await conn.hmget(key, sub_keys)
            return [item.decode("UTF-8") for item in result if item]

    async def _delete_keys_from_dict(self, key: str, sub_keys: List[str]):
        async with self._get_redis() as conn:
            await conn.hdel(key, *sub_keys)

    async def _get_value_from_dict(self, key: str, sub_key: str) -> str | None:
        async with self._get_redis() as conn:
            result = await conn.hmget(key, [sub_key])
            return result[0].decode("UTF-8") if result and result[0] else None

    async def _get_key_value_from_dict(self, key: str, sub_key: str) -> CreateSchemaType:
        async with self._get_redis() as conn:
            result = await conn.hget(key, sub_key)
            return self.converter.decode_from_bytes(result)

    async def _update_key_value_in_dict(self, key: str, sub_key: str, data: str):
        async with self._get_redis() as conn:
            await conn.hset(key, sub_key, data)

    async def _increment_value_in_dict(self, key: str, sub_key: str, value: int) -> int:
        async with self._get_redis() as conn:
            return await conn.hincrby(key, sub_key, value)

    async def _get_list(self, key) -> Optional[List[str | int]]:
        async with self._get_redis() as conn:
            result = await conn.lrange(key, 0, -1)
            return [item.decode("UTF-8") for item in result] if result else None

    async def _get_enumerate_list(self, key) -> Dict[int, str]:
        async with self._get_redis() as conn:
            result = await conn.lrange(key, 0, -1)
            return {i + 1: item.decode("UTF-8") for i, item in enumerate(result)} if result else {}

    async def _get_last_element_from_list(self, key) -> str | None:
        async with self._get_redis() as conn:
            result = await conn.lrange(key, -1, -1)
            return result[0] if result else None

    async def _add_to_list(self, key: str, *values: str | int) -> int:
        async with self._get_redis() as conn:
            return await conn.rpush(key, *values)

    async def _remove_from_list(self, key: str, value: str):
        async with self._get_redis() as conn:
            await conn.lrem(key, 0, value)

    async def _save_model(self, key: str, data: CreateSchemaType):
        data = self.converter.encode_to_dict(data)
        await self._save_dict(key, data)

    async def _get_model(self, key: str) -> CreateSchemaType | None:
        result = await self._get_dict(key)
        return self.converter.decode_from_dict(result) if result else None

    async def _update_model(self, key: str, update: UpdateSchemaType):
        update = self.converter.encode_to_dict(update, exclude_unset=True)
        async with self._get_redis() as conn:
            await conn.hset(name=key, mapping=update)

    async def _add_to_set(self, key: str, *values: str):
        async with self._get_redis() as conn:
            await conn.sadd(key, *values)

    async def _get_set(self, key: str) -> Optional[List[str]]:
        async with self._get_redis() as conn:
            result = await conn.smembers(key)
        return [item.decode("UTF-8") for item in result] if result else None


class EventChannel(StrEnum):
    test_run = "test_run"


class EventType(StrEnum):
    current = "current"
    update = "update"


class Event(BaseModel):
    channel: EventChannel


class RedisChannel:
    CHANNEL_SHUTDOWN_SIGNAL = "SHUTDOWN"

    @staticmethod
    async def _write(key: str, message: Union[bytes, memoryview, str, int, float]):
        conn = await redis.get_connection()
        await conn.xadd(key, {"data": message})

    async def _close(self, key: str):
        conn = await redis.get_connection()
        await conn.xadd(key, {"data": self.CHANNEL_SHUTDOWN_SIGNAL})
        asyncio.create_task(delete_key_with_delay(conn, key, delay_seconds=60 * 5))

    async def _listen(self, key: str) -> AsyncIterator[Union[bytes, memoryview, str, int, float]]:
        conn = await redis.get_connection()
        last_id = "0"
        while True:
            if not await redis_key_exist_with_wait(conn, key):
                break
            if messages := await conn.xread(streams={key: last_id}, block=0):
                for _, entries in messages:
                    for msg_id, message in entries:
                        last_id = msg_id
                        decoded_message = message[b"data"].decode("UTF-8")
                        if decoded_message == self.CHANNEL_SHUTDOWN_SIGNAL:
                            await conn.delete(key)
                            break
                        else:
                            yield decoded_message

    async def _proxy_to_ws(self, key: str, websocket: WebSocket):
        async for message in self._listen(key):
            await websocket.send_text(message)

    async def proxy_to_ws(self, *args, **kwargs):
        raise NotImplementedError
