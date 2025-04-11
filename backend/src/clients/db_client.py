import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, List, Optional, Tuple, Union

import aiomysql
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from src.modules.auto_test.utils.add_auto_test_warinig import add_warning_to_test
from src.utils.rate_limiter import Singleton


class DateBaseClient(metaclass=Singleton):
    def __init__(
        self, host: str, port: int, user: str, password: str, database: str, pool_size: int, connect_timeout: int = 100
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool_size = pool_size
        self.connect_timeout = connect_timeout  # The timeout for connecting to the database in seconds.
        self.connections_pool: Optional[aiomysql.pool.Pool] = None
        self.create_pull_lock = asyncio.Lock()

    async def connect(self):
        self.connections_pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            maxsize=self.pool_size,
            connect_timeout=self.connect_timeout,
            pool_recycle=60 * 5,
            autocommit=True,
        )

    @asynccontextmanager
    async def connection_cursor(self) -> AsyncGenerator[aiomysql.cursors.SSDictCursor, None]:
        async with self.create_pull_lock:
            if not self.connections_pool:
                await self.connect()

        async with self.connections_pool.acquire() as conn:
            async with conn.cursor(aiomysql.cursors.SSDictCursor) as cur:
                yield cur

    @retry(
        retry=retry_if_exception_type(aiomysql.OperationalError),
        stop=stop_after_attempt(2),
        wait=wait_fixed(3),
        after=lambda retry_call_state: add_warning_to_test(
            f"{retry_call_state.attempt_number} attempt to execute query "
            f"fails with exception: {retry_call_state.outcome.exception()}"
        ),
        reraise=True,
    )
    async def fetch_all(self, query: str, args: Optional[Union[Tuple, List, Dict]] = None):
        result = []
        async with self.connection_cursor() as cur:
            await cur.execute(query, args)
            while True:
                rows = await cur.fetchmany(1000)
                if not rows:
                    break
                result.extend(rows)
        return result

    @retry(
        retry=retry_if_exception_type(aiomysql.OperationalError),
        stop=stop_after_attempt(2),
        wait=wait_fixed(3),
        after=lambda retry_call_state: add_warning_to_test(
            f"{retry_call_state.attempt_number} attempt to execute query "
            f"fails with exception: {retry_call_state.outcome.exception()}"
        ),
        reraise=True,
    )
    async def fetch_one(self, query: str, args: Optional[Union[Tuple, List, Dict]] = None):
        async with self.connection_cursor() as cur:
            await cur.execute(query, args)
            return await cur.fetchone()

    async def update(self, query: str):
        async with self.connection_cursor() as cur:
            await cur.execute(query)

    async def close(self):
        if self.connections_pool:
            self.connections_pool.close()
            await self.connections_pool.wait_closed()
            self.connections_pool = None

    def __del__(self):
        self.connections_pool and self.connections_pool.close()
        self.connections_pool = None
