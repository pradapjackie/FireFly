import asyncio
from asyncio import Lock, Semaphore
from typing import Dict, Literal, Optional

from self_limiters import Semaphore as RedisSemaphore

from src.core.config import settings
from src.modules.auto_test.contexts import test_run_context
from src.modules.script_runner.contexts import script_context


class Singleton(type):
    """
    This class produces only one instance for each test run per each event loop
    """

    _instances_by_run_and_loop = {}

    @classmethod
    def clear_by_test_run(cls, run_id: str):
        cls._instances_by_run_and_loop.pop(run_id, None)

    @staticmethod
    def _in_auto_test_context() -> bool:
        return test_run_context and test_run_context.get(None) is not None

    @staticmethod
    def _in_script_context() -> bool:
        return script_context and script_context.get(None) is not None

    def __call__(cls, *args, **kwargs):
        if cls._in_auto_test_context():
            context_id = test_run_context.get().id
        elif cls._in_script_context():
            context_id = script_context.get().execution_id
        else:
            raise RuntimeError("Singleton instance can be created only in autotest or script context")
        if context_id not in cls._instances_by_run_and_loop:
            cls._instances_by_run_and_loop[context_id] = {}

        loop_id = asyncio.get_running_loop()
        if loop_id not in cls._instances_by_run_and_loop[context_id]:
            cls._instances_by_run_and_loop[context_id][loop_id] = {}

        if cls not in cls._instances_by_run_and_loop[context_id][loop_id]:
            cls._instances_by_run_and_loop[context_id][loop_id][cls] = super().__call__(*args, **kwargs)

        return cls._instances_by_run_and_loop[context_id][loop_id][cls]


class RateLimiter(Semaphore, metaclass=Singleton):
    async def acquire(self, timeout: Optional[int] = 10 * 60) -> Literal[True]:
        return await asyncio.wait_for(super().acquire(), timeout=timeout)


class SingleLock(Lock, metaclass=Singleton):
    async def acquire(self, timeout: Optional[int] = 10 * 60):
        return await asyncio.wait_for(super().acquire(), timeout=timeout)


class RedisLock:
    def __init__(self, name: str, timeout: Optional[int] = 10 * 60):
        self.semaphore = RedisSemaphore(
            name, capacity=1, max_sleep=timeout, expiry=timeout, redis_url=settings.REDIS_CACHE
        )

    async def __aenter__(self):
        await self.semaphore.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.semaphore.__aexit__(exc_type, exc_val, exc_tb)


class RedisRateLimiter:
    def __init__(self, capacity: int, timeout: Optional[int] = 10 * 60):
        self.semaphore = RedisSemaphore(
            self.__class__.__name__,
            capacity=capacity,
            max_sleep=timeout,
            expiry=timeout,
            redis_url=settings.REDIS_CACHE,
        )

    async def acquire(self):
        await self.semaphore.__aenter__()

    async def release(self, exc_type=None, exc_val=None, exc_tb=None):
        await self.semaphore.__aexit__(exc_type, exc_val, exc_tb)

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release(exc_type, exc_val, exc_tb)


class LockManager(metaclass=Singleton):
    locks: Dict[str, SingleLock] = {}

    def get_lock(self, name: str) -> SingleLock:
        if not self.locks.get(name):
            self.locks[name] = type(f"AsyncLock_{name}", (SingleLock,), {})()
        return self.locks[name]


class RateLimiterManager(metaclass=Singleton):
    def __init__(self, value: int):
        self.value = value

    limits: Dict[str, RateLimiter] = {}

    def get_limit(self, name: str) -> RateLimiter:
        if not self.limits.get(name):
            self.limits[name] = type(f"RateLimiter_{name}", (RateLimiter,), {})(self.value)
        return self.limits[name]
