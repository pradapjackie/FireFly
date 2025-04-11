from typing import Dict, List

from fastapi import WebSocket

from src.cache.base import RedisChannel
from src.cache.base_event_manager import EventManager
from src.schemas.script_runner.script_events import (
    EnvUsedUpdate,
    ErrorsEvent,
    IntermediateErrorsEvent,
    IntermediateResultEvent,
    LogEvent,
    LogMessage,
    ResultEvent,
    ScriptEvent,
    StatusEvent,
)
from src.schemas.script_runner.script_history import ScriptError, ScriptResult, ScriptStatusEnum


class ScriptEventChannel(RedisChannel):
    async def _write_event(self, execution_id: str, event: ScriptEvent):
        await self._write(f"script:{execution_id}:channel", event.model_dump_json())

    async def close_channel(self, execution_id):
        await self._close(f"script:{execution_id}:channel")

    async def proxy_to_ws(self, execution_id: str, websocket: WebSocket):
        await super()._proxy_to_ws(f"script:{execution_id}:channel", websocket)

    async def update_status(self, script_id: str, execution_id: str, status: ScriptStatusEnum):
        event = StatusEvent(script_id=script_id, message=status)
        await self._write_event(execution_id, event)

    async def add_log(self, script_id: str, execution_id: str, index: int, line: str):
        event = LogEvent(script_id=script_id, message=LogMessage(index=index, line=line))
        await self._write_event(execution_id, event)

    async def add_result(self, script_id: str, execution_id: str, result: ScriptResult):
        event = ResultEvent(script_id=script_id, message=result)
        await self._write_event(execution_id, event)

    async def add_intermediate_result(
        self, script_id: str, execution_id: str, result: ScriptResult | Dict[int, ScriptResult]
    ):
        event = IntermediateResultEvent(script_id=script_id, message=result)
        await self._write_event(execution_id, event)

    async def add_errors(self, script_id: str, execution_id: str, errors: List[ScriptError]):
        event = ErrorsEvent(script_id=script_id, message=errors)
        await self._write_event(execution_id, event)

    async def add_intermediate_errors(self, script_id: str, execution_id: str, errors: List[ScriptError]):
        event = IntermediateErrorsEvent(script_id=script_id, message=errors)
        await self._write_event(execution_id, event)

    async def add_env_used(self, script_id: str, execution_id: str, env_used: Dict[str, str]):
        event = EnvUsedUpdate(script_id=script_id, message=env_used)
        await self._write_event(execution_id, event)


class ScriptEventManager(EventManager):
    def __init__(self):
        super().__init__(ScriptEventChannel())
