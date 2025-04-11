from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field

from src.utils.pydantic_helper import CamelCaseModel

from .common import By


class FindElementRequest(BaseModel):
    using: By
    value: str


class FindChildElementRequest(FindElementRequest):
    id: str


class Element(BaseModel):
    id: str = Field(alias="ELEMENT")


class SendTextRequest(BaseModel):
    value: List[str] | None = None
    text: str | None = None


class ElementLocation(BaseModel):
    x: int
    y: int


class ElementSize(BaseModel):
    width: int
    height: int


class ActionsChain(BaseModel):
    actions: List[dict]


class ExecuteScriptPayload(BaseModel):
    script: str
    args: list[dict]


class ScriptArgs(CamelCaseModel):
    pass


class ScrollDirection(StrEnum):
    up = "up"
    down = "down"


class ScrollToElementScript(ScriptArgs):
    predicate_string: str
    direction: ScrollDirection
    to_visible: bool = True
