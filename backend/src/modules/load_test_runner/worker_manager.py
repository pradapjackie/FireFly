import asyncio
import inspect
from collections import defaultdict
from functools import partial
from typing import Any, Callable, Coroutine, DefaultDict, Dict, List, Type

from src.cache.load_test.internal_event_channel import LoadTestInternalEventChannel
from src.cache.load_test.report import LoadTestReportCache
from src.cache.load_test.tasks import LoadTestTaskCache
from src.cache.load_test.workers import LoadTestWorkerCache
from src.modules.environment.env import env
from src.modules.load_test_runner.charts.base import BaseChart
from src.modules.load_test_runner.collector import Collector
from src.modules.load_test_runner.contexts import LoadTestExecutionContext, load_test_context
from src.modules.load_test_runner.load_test_abs import LoadTestAbc
from src.schemas.load_test.load_test import LoadTest
from src.schemas.load_test.load_test_events import LoadTestInternalEventTypeEnum
from src.schemas.load_test.load_test_history import (
    LoadTestTaskStatusEnum,
    LoadTestWorkerStatusEnum,
    WorkerFinishedException,
)


class LoadTestWorkerManager:
    def __init__(self, load_test_id: str, execution_id: str, worker_id: str):
        self.load_test_id = load_test_id
        self.execution_id = execution_id
        self.worker_id = worker_id
        self.collector = Collector()
        self.report_cache = LoadTestReportCache(load_test_id)
        self.worker_cache = LoadTestWorkerCache(load_test_id, execution_id)
        self.tasks_cache = LoadTestTaskCache(load_test_id, execution_id)
        self.command_channel = LoadTestInternalEventChannel(load_test_id, execution_id)

        self.teardown_callbacks: DefaultDict[str, List[Callable[..., Coroutine[Any, Any, None]]]] = defaultdict(list)

    def start_sync(self):
        asyncio.get_event_loop().run_until_complete(self.start())

    async def listen_for_stop_event(self):
        async for message in self.command_channel.listen():
            if message.type == LoadTestInternalEventTypeEnum.stop_all_workers:
                raise WorkerFinishedException
            if message.type == LoadTestInternalEventTypeEnum.stop_specific_worker and message.data == self.worker_id:
                print("stop_specific_worker", message.data, self.worker_id, flush=True)
                raise WorkerFinishedException

    async def start(self):
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.listen_for_stop_event())
                tg.create_task(self._start())
        except* WorkerFinishedException:
            pass
        finally:
            await asyncio.gather(
                *[
                    self.run_one_task_teardown(task_id, callback_list)
                    for task_id, callback_list in self.teardown_callbacks.items()
                ]
            )
            await self.worker_cache.update_status(self.worker_id, LoadTestWorkerStatusEnum.finished)

    async def _start(self):
        load_test_context.set(LoadTestExecutionContext(load_test_id=self.load_test_id, execution_id=self.execution_id))
        load_test_report = await self.report_cache.get(self.execution_id)
        load_test = await self.collector.collect_load_test_by_id(self.load_test_id, load_test_report.root_folder)
        env.prime_environment(
            env_name=load_test_report.env_name,
            setting_overwrite=load_test_report.setting_overwrite,
            env_user_contexts=[load_test_context],
        )
        self.prime_charts_with_names(load_test.callable)
        input_params = self.collector.process_input_params(load_test.params, load_test_report.params)
        concurrency = load_test_report.config_values.concurrency_within_a_single_worker
        await self.worker_cache.update_status(self.worker_id, LoadTestWorkerStatusEnum.working)
        await self.tasks_cache.create_multi(
            {f"{self.worker_id}:{i}": LoadTestTaskStatusEnum.pending for i in range(concurrency)}
        )
        await asyncio.gather(
            *[self.start_one_task(load_test, input_params, f"{self.worker_id}:{i}") for i in range(concurrency)]
        )

    async def start_one_task(self, load_test: LoadTest, input_params: Dict, task_id: str):
        load_test_instance = load_test.callable(**input_params)
        await self.run_one_task_setup(load_test_instance, task_id)
        await self.run_one_task_worker(load_test_instance, task_id)

    async def run_one_task_setup(self, load_test_instance: LoadTestAbc, task_id: str):
        await self.tasks_cache.update_status(task_id, LoadTestTaskStatusEnum.setup)
        for test_parent in load_test_instance.__class__.__mro__[::-1]:
            if issubclass(test_parent, LoadTestAbc) and "setup" in test_parent.__dict__.keys():
                await test_parent.setup(load_test_instance)
                if "teardown" in test_parent.__dict__.keys():
                    self.teardown_callbacks[task_id].append(partial(test_parent.teardown, load_test_instance))

    async def run_one_task_teardown(
        self, task_id: str, teardown_callbacks: List[Callable[..., Coroutine[Any, Any, None]]]
    ):
        await self.tasks_cache.update_status(task_id, LoadTestTaskStatusEnum.teardown)
        for callback in teardown_callbacks:
            await callback()
        await self.tasks_cache.update_status(task_id, LoadTestTaskStatusEnum.finished)

    async def run_one_task_worker(self, load_test_instance: LoadTestAbc, task_id: str):
        await self.tasks_cache.update_status(task_id, LoadTestTaskStatusEnum.working)
        await load_test_instance.worker()

    @staticmethod
    def prime_charts_with_names(test_class: Type[LoadTestAbc]):
        if config_cls := getattr(test_class, "Charts", None):
            for alias, field in inspect.getmembers(config_cls, predicate=lambda x: isinstance(x, BaseChart)):
                field.name = alias
