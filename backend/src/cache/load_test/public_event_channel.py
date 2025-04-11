from typing import Any

from fastapi import WebSocket

from src.cache.base import RedisChannel
from src.cache.base_event_manager import EventManager
from src.schemas.load_test.load_test_events import (
    ChartMessage,
    ExecutionMessage,
    LoadTestChartEvent,
    LoadTestEvent,
    LoadTestExecutionEvent,
    LoadTestTaskHistoryEvent,
    LoadTestWorkerEvent,
    TaskHistoryMessage,
    WorkerMessage,
)
from src.schemas.load_test.load_test_history import (
    LoadTestHistoryUpdate,
    LoadTestTaskStatusHistory,
    LoadTestWorkerStatusEnum,
)


class LoadTestPublicEventChannel(RedisChannel):
    async def _write_event(self, execution_id: str, event: LoadTestEvent):
        await self._write(f"load_test:{execution_id}:channel", event.model_dump_json())

    async def proxy_to_ws(self, execution_id: str, websocket: WebSocket):
        await super()._proxy_to_ws(f"load_test:{execution_id}:channel", websocket)

    async def update_execution_status(self, load_test_id: str, execution_id: str, update: LoadTestHistoryUpdate):
        event = LoadTestExecutionEvent(
            data=ExecutionMessage(load_test_id=load_test_id, update=update.model_dump(exclude_unset=True))
        )
        await self._write_event(execution_id, event)

    async def update_worker_status(
        self, load_test_id: str, execution_id: str, worker_id: str, status: LoadTestWorkerStatusEnum
    ):
        event = LoadTestWorkerEvent(data=WorkerMessage(load_test_id=load_test_id, worker_id=worker_id, status=status))
        await self._write_event(execution_id, event)

    async def update_task_status_history(
        self, load_test_id: str, execution_id: str, now_string: str, data: LoadTestTaskStatusHistory
    ):
        event = LoadTestTaskHistoryEvent(
            data=TaskHistoryMessage(load_test_id=load_test_id, now_string=now_string, data=data)
        )
        await self._write_event(execution_id, event)

    async def update_task_chart_data(self, load_test_id: str, execution_id: str, chart_name: str, data: Any):
        event = LoadTestChartEvent(data=ChartMessage(load_test_id=load_test_id, chart_name=chart_name, data=data))
        await self._write_event(execution_id, event)


class LoadTestEventManager(EventManager):
    def __init__(self):
        super().__init__(LoadTestPublicEventChannel())
