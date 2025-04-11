from enum import StrEnum
from pathlib import Path
from typing import Any, Awaitable, Callable, Type

from pydantic import BaseModel


class ReCollectRequest(BaseModel):
    root_folder: str | None = None


class CollectedPath(BaseModel):
    name: str
    path: Path


class CollectedObject(CollectedPath):
    root_folder: str
    callable: Type | Callable[[...], Awaitable[Any]]

    @property
    def id(self) -> str:
        raise NotImplementedError(f"Id property not implemented for {self.__class__.__name__}")


class CollectObjectTypes(StrEnum):
    class_ = "class"
    async_function = "async_function"


class SubscribeMessage(BaseModel):
    execution_id: str | None = None
    load_test_id: str | None = None


class SuccessfulSubscribeMessage(SubscribeMessage):
    type: str = "successful_subscribe"
