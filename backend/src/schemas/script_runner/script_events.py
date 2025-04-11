from enum import StrEnum
from typing import Dict, List

from pydantic import BaseModel

from src.schemas.script_runner.script_history import ScriptError, ScriptResult, ScriptStatusEnum


class EventTypeEnum(StrEnum):
    status = "status"
    log = "log"
    result = "result"
    intermediate_result = "intermediate_result"
    errors = "errors"
    intermediate_errors = "intermediate_errors"
    env_used = "env_used"


class ScriptEvent(BaseModel):
    type: EventTypeEnum


class LogMessage(BaseModel):
    index: int
    line: str


class StatusEvent(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.status
    script_id: str
    message: ScriptStatusEnum


class LogEvent(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.log
    script_id: str
    message: LogMessage


class ResultEvent(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.result
    script_id: str
    message: ScriptResult


class IntermediateResultEvent(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.intermediate_result
    script_id: str
    message: ScriptResult | Dict[int, ScriptResult]


class ErrorsEvent(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.errors
    script_id: str
    message: List[ScriptError]


class IntermediateErrorsEvent(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.intermediate_errors
    script_id: str
    message: List[ScriptError]


class EnvUsedUpdate(ScriptEvent):
    type: EventTypeEnum = EventTypeEnum.env_used
    script_id: str
    message: Dict[str, str]
