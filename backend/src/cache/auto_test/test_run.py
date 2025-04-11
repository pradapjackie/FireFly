from fastapi import WebSocket
from pydantic import BaseModel

from src.cache.base import CacheBase, Event, EventChannel, EventType, RedisChannel
from src.schemas.auto_test.common import ResultByStatus
from src.schemas.auto_test.test_run import TestRun, TestRunStatus, TestRunUpdate


class TestRunCache(CacheBase[TestRun, TestRunUpdate]):
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.root_key = f"{run_id}:info"
        super().__init__(TestRun)

    async def create(self, data: TestRun):
        data = data.model_copy()
        result_by_status = data.result_by_status.model_dump()
        data.result_by_status = None
        await self._save_model(self.root_key, data)
        await self._save_dict(f"{self.root_key}:result", result_by_status)

    async def get(self) -> TestRun:
        test_run = await self._get_model(self.root_key)
        result_by_status = await self._get_decoded_dict(f"{self.root_key}:result")
        test_run.result_by_status = ResultByStatus(**result_by_status)
        return test_run

    async def get_status(self) -> TestRunStatus:
        status = await self._get_value_from_model(self.root_key, "status")
        return TestRunStatus(status)

    async def update(self, update: TestRunUpdate):
        await self._update_model(self.root_key, update)

    async def increment_by(self, status_name: str, value: int):
        await self._increment_value_in_dict(f"{self.root_key}:result", status_name, value)


class TestRunEventData(BaseModel):
    status: TestRunStatus


class TestRunEvent(Event):
    channel: EventChannel = EventChannel.test_run
    type: EventType
    data: TestRunEventData


class TestRunChannel(RedisChannel):
    def __init__(self, run_id: str):
        self.key = f"{run_id}:channel"

    async def update(self, status: TestRunStatus):
        event = TestRunEvent(type=EventType.update, data=TestRunEventData(status=status))
        await self._write(self.key, event.model_dump_json())

    async def send_current(self, status: TestRunStatus):
        event = TestRunEvent(type=EventType.current, data=TestRunEventData(status=status))
        await self._write(self.key, event.model_dump_json())

    async def proxy_to_ws(self, websocket: WebSocket):
        await super()._proxy_to_ws(self.key, websocket)
