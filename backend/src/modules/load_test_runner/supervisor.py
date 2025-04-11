import asyncio
from typing import Dict, List

import pendulum

from src.cache.load_test.internal_event_channel import LoadTestInternalEventChannel
from src.cache.load_test.public_event_channel import LoadTestPublicEventChannel
from src.cache.load_test.report import LoadTestReportCache
from src.cache.load_test.tasks import LoadTestTaskCache
from src.schemas.load_test.load_test_events import LoadTestInternalEventTypeEnum, WorkerStatusInternalUpdate
from src.schemas.load_test.load_test_history import (
    LoadTestHistoryUpdate,
    LoadTestStatusEnum,
    LoadTestTaskStatusHistory,
    LoadTestWorkerStatusEnum,
    SupervisorFinishedException,
)


class LoadTestSupervisor:
    def __init__(self, load_test_id: str, execution_id: str):
        self.load_test_id = load_test_id
        self.execution_id = execution_id
        self.report_cache = LoadTestReportCache(load_test_id)
        self.internal_channel = LoadTestInternalEventChannel(load_test_id, execution_id)
        self.public_channel = LoadTestPublicEventChannel()
        self.task_cache = LoadTestTaskCache(load_test_id, execution_id)

        self.stop_event = asyncio.Event()
        self.supervisor_tasks: List[asyncio.Task] = []

        self.execution_status = LoadTestStatusEnum.pending
        self.workers: Dict[str, LoadTestWorkerStatusEnum] = {}

    def start_sync(self):
        asyncio.get_event_loop().run_until_complete(self.start())

    async def listen_for_events(self):
        async for message in self.internal_channel.listen():
            match message.type:
                case LoadTestInternalEventTypeEnum.worker_status_update:
                    await self.handle_worker_status_update(message.data)
                case LoadTestInternalEventTypeEnum.start_task_updates:
                    self.supervisor_tasks.append(asyncio.create_task(self.task_status_regular_update()))
                    await asyncio.sleep(0)  # Start task immediately

    async def start(self):
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.wait_for_stop_event())
                tg.create_task(self.listen_for_events())
        except* SupervisorFinishedException:
            pass
        finally:
            for task in self.supervisor_tasks:
                not task.done() and task.cancel()
            await self.update_execution_status(LoadTestStatusEnum.finished)

    async def wait_for_stop_event(self):
        await self.stop_event.wait()
        raise SupervisorFinishedException

    async def task_status_regular_update(self):
        while True:
            current_task_state = await self.task_cache.get_current_status_map()
            now_time = pendulum.now("UTC").format("YYYY-MM-DD HH:mm:ss")
            task_history = LoadTestTaskStatusHistory(**current_task_state)
            await self.task_cache.add_status_history(now_time, task_history)
            await self.public_channel.update_task_status_history(
                self.load_test_id, self.execution_id, now_time, task_history
            )
            if all((status == LoadTestWorkerStatusEnum.finished for status in self.workers.values())):
                self.execution_status = LoadTestStatusEnum.finished
                self.stop_event.set()
            await asyncio.sleep(3)

    async def handle_worker_status_update(self, data: WorkerStatusInternalUpdate):
        await self.public_channel.update_worker_status(
            self.load_test_id, self.execution_id, data.worker_id, data.status
        )
        self.workers[data.worker_id] = data.status
        if self.execution_status == LoadTestStatusEnum.pending and data.status == LoadTestWorkerStatusEnum.working:
            await self.update_execution_status(LoadTestStatusEnum.running)

    async def update_execution_status(self, new_status: LoadTestStatusEnum):
        self.execution_status = new_status
        update = LoadTestHistoryUpdate(status=new_status)
        await self.report_cache.update(self.execution_id, update)
        await self.public_channel.update_execution_status(self.load_test_id, self.execution_id, update)
