from typing import Optional, Self

from aiomcache import Client, ClientException

# noinspection PyProtectedMember
from aiomcache.client import acquire

# noinspection PyProtectedMember
from aiomcache.pool import Connection
from tenacity import retry, retry_if_result, stop_after_attempt, stop_after_delay, wait_fixed

from src.modules.auto_test.step_manager import step
from src.modules.auto_test.utils.add_auto_test_warinig import add_warning_to_test


def is_none(value):
    return value is None


class MemcachedClient(Client):
    def __init__(self, host: str, port: int = 11211, *args, **kwargs):
        super().__init__(host, port, *args, **kwargs)
        self.host = host
        self.port = port

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _get(self, conn: Optional[Connection], key: str) -> Optional[bytes]:
        async with step(f"Get key {key} from {self.host}:{self.port}"):
            value = None
            conn.writer.write(f"get {key}\r\n".encode("UTF-8"))
            line = await conn.reader.readline()

            while line != b"END\r\n":
                terms = line.split()

                if terms[0] == b"VALUE":
                    if value:
                        raise ClientException("received too values received")
                    length = int(terms[3])
                    value = (await conn.reader.readexactly(length + 2))[:-2]
                else:
                    raise ClientException("get failed", line)

                line = await conn.reader.readline()

            return value

    @acquire
    async def get(self, conn: Optional[Connection], key: str) -> Optional[str]:
        value = await self._get(conn, key)
        return value.decode("UTF-8") if value else None

    @acquire
    async def get_raw(self, conn: Optional[Connection], key: str) -> Optional[bytes]:
        value = await self._get(conn, key)
        return value if value else None

    async def get_key(self, key) -> Optional[str]:
        async with step(f"Get key: {key} from {self.host}:{self.port}"):
            return await self.get(key)

    @retry(
        retry=retry_if_result(is_none),
        stop=(stop_after_delay(60) | stop_after_attempt(5)),
        wait=wait_fixed(3),
        after=lambda retry_call_state: add_warning_to_test(
            f"{retry_call_state.attempt_number} attempt to get key from memcached "
            f"fails with exception: {retry_call_state.outcome.exception()}"
        ),
        reraise=True,
    )
    async def get_with_retry(self, key: str) -> str:
        return await self.get_key(key)

    async def delete_key(self, key: str) -> bool:
        async with step(f"Delete key {key} from {self.host}:{self.port}"):
            return await self.delete(key.encode("UTF-8"))

    async def set_raw(self, key: str, value: bytes, exptime: int = 0) -> bool:
        async with step(f"Set key {key} to {self.host}:{self.port}"):
            return await super().set(key.encode("UTF-8"), value, exptime)
