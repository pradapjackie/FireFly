import json
from typing import AsyncIterator

from src.cache.base import RedisChannel
from src.schemas.load_test.load_test_events import (
    LoadTestInternalEvent,
    LoadTestInternalEventTypeEnum,
    LoadTestStartTaskUpdatesEvent,
    LoadTestStopSpecificWorkerEvent,
    LoadTestStopWorkersEvent,
    LoadTestWorkerStatusUpdate,
    WorkerStatusInternalUpdate,
)
from src.schemas.load_test.load_test_history import LoadTestWorkerStatusEnum


class LoadTestInternalEventChannel(RedisChannel):
    def __init__(self, load_test_id: str, execution_id: str):
        self.load_test_id = load_test_id
        self.execution_id = execution_id
        self.key = f"load_test:{execution_id}:internal_channel"

    async def _write_event(self, event: LoadTestInternalEvent):
        await self._write(self.key, event.model_dump_json())

    async def send_stop_workers_event(self):
        await self._write_event(LoadTestStopWorkersEvent())

    async def send_stop_specific_worker_event(self, worker_id):
        await self._write_event(LoadTestStopSpecificWorkerEvent(data=worker_id))

    async def update_worker_status(self, worker_id: str, status: LoadTestWorkerStatusEnum):
        event = LoadTestWorkerStatusUpdate(data=WorkerStatusInternalUpdate(worker_id=worker_id, status=status))
        await self._write_event(event)

    async def start_task_updates(self):
        await self._write_event(LoadTestStartTaskUpdatesEvent())

    async def listen(self) -> AsyncIterator[LoadTestInternalEvent]:
        async for message in self._listen(self.key):
            message = json.loads(message)
            match message["type"]:
                case LoadTestInternalEventTypeEnum.stop_all_workers:
                    yield LoadTestStopWorkersEvent(**message)
                case LoadTestInternalEventTypeEnum.stop_specific_worker:
                    yield LoadTestStopSpecificWorkerEvent(**message)
                case LoadTestInternalEventTypeEnum.worker_status_update:
                    yield LoadTestWorkerStatusUpdate(**message)
                case LoadTestInternalEventTypeEnum.start_task_updates:
                    yield LoadTestStartTaskUpdatesEvent(**message)
