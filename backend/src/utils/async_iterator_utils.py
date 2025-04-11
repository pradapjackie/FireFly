from __future__ import annotations

import asyncio
from contextlib import AsyncExitStack
from inspect import getdoc
from typing import AsyncIterator, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar

from async_timeout import timeout

from src.modules.auto_test.step_manager import step

IterableItem = TypeVar("IterableItem")


async def accumulate_result_from_generator(
    iterable: AsyncIterator[IterableItem], timeout_between_events: Optional[float] = None
) -> List[IterableItem]:
    result = []
    try:
        while True:
            event = await asyncio.wait_for(iterable.__aiter__().__anext__(), timeout_between_events)
            result.append(event)
    except (asyncio.TimeoutError, StopAsyncIteration):
        return result


class BackgroundSubscription:
    def __init__(self, name: str, subscription: AsyncIterator[IterableItem]):
        self.name = name
        self._subscription = subscription
        self._background_task: Optional[asyncio.Task] = None
        self._data: List[IterableItem] = []

    async def _accumulate_subscription_iterator(self):
        async for message in self._subscription:
            self._data.append(message)

    async def wait_for(
        self,
        predicate: Callable[[List[IterableItem], ...], Tuple[bool, List[IterableItem]]],
        timeout_sec: int,
        **predicate_kwargs,
    ) -> List[IterableItem]:
        try:
            async with timeout(int(timeout_sec)):
                while True:
                    is_match, events = predicate(self._data, **predicate_kwargs)
                    if is_match:
                        return events
                    await asyncio.sleep(0.2)
        except asyncio.TimeoutError as e:
            predicate_description = getdoc(predicate) or predicate.__name__
            received_data = "\n" + "\n".join([str(item) for item in self._data])
            raise asyncio.TimeoutError(
                f"""
                Subscription: {self.name}
                We wait for "{predicate_description}" for {timeout_sec} seconds without success.
                Received data: {received_data}
                """
            ) from e

    def clear(self):
        self._data = []

    def get_data(self) -> List[IterableItem]:
        return self._data

    async def __aenter__(self) -> BackgroundSubscription:
        async with step(f"Start {self.name} subscription"):
            self._background_task = asyncio.create_task(self._accumulate_subscription_iterator())
            await asyncio.sleep(0)  # Start task immediately
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async with step(f"End {self.name} subscription"):
            self._background_task and self._background_task.cancel()


class BackgroundSubscriptions:
    def __init__(self, subscriptions: Dict[str, AsyncIterator[IterableItem]]):
        self._subscriptions = subscriptions
        self._background_subscriptions_stack = AsyncExitStack()
        self._background_subscriptions: List[BackgroundSubscription] = []

    async def __aenter__(self) -> List[BackgroundSubscription]:
        for name, subscription in self._subscriptions.items():
            background_subscription = BackgroundSubscription(name, subscription)
            self._background_subscriptions.append(background_subscription)
            await self._background_subscriptions_stack.enter_async_context(background_subscription)
        return self._background_subscriptions

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._background_subscriptions_stack.__aexit__(exc_type, exc_val, exc_tb)


def batch(iterable: List, n=1) -> Iterator[List]:
    length = len(iterable)
    for ndx in range(0, length, n):
        yield iterable[ndx : min(ndx + n, length)]


_T = TypeVar("_T")


async def a_enumerate(iterable: AsyncIterator[_T], start=0) -> AsyncIterator[Tuple[int, _T]]:
    """Asynchronously enumerate an async iterator from a given start value"""
    i = start
    async for item in iterable:
        yield i, item
        i += 1
