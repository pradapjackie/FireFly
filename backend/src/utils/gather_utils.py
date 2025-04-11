import asyncio
from typing import Coroutine, List, Tuple, TypeVar

T = TypeVar("T")


async def semaphore_gather(
    limit: int, coroutines: List[Coroutine[None, None, T]], return_exceptions=False
) -> List[T | BaseException]:
    semaphore = asyncio.Semaphore(limit)

    async def _wrap_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(_wrap_coro(coro) for coro in coroutines), return_exceptions=return_exceptions)


async def gather_with_exceptions(coroutines: List[Coroutine[None, None, T]]) -> Tuple[List[T], List[BaseException]]:
    result = await asyncio.gather(*coroutines, return_exceptions=True)
    success = [item for item in result if not isinstance(item, BaseException)]
    errors = [item for item in result if isinstance(item, BaseException)]
    return success, errors


async def gather_with_exceptions_and_semaphore(
    limit: int, coroutines: List[Coroutine[None, None, T]]
) -> Tuple[List[T], List[BaseException]]:
    result = await semaphore_gather(limit, coroutines, return_exceptions=True)
    success = [item for item in result if not isinstance(item, BaseException)]
    errors = [item for item in result if isinstance(item, BaseException)]
    return success, errors
