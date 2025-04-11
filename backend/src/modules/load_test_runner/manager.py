import asyncio
from contextlib import asynccontextmanager

from fastapi import HTTPException

from src.cache.load_test.current import LoadTestCurrentCache
from src.cache.load_test.internal_event_channel import LoadTestInternalEventChannel
from src.cache.load_test.report import LoadTestReportCache
from src.cache.load_test.workers import LoadTestWorkerCache
from src.core.celery_app import get_current_celery_capacity
from src.modules.load_test_runner.collector import Collector
from src.modules.load_test_runner.contexts import LoadTestExecutionContext, load_test_context
from src.schemas.load_test.load_test import LoadTestConfig
from src.schemas.load_test.load_test_history import LoadTestWorkerStatusEnum
from src.tasks import start_load_task, start_load_test_supervisor


class LoadTestManager:
    def __init__(self, load_test_id: str):
        self.load_test_id = load_test_id
        self.collector = Collector()
        self.report_cache = LoadTestReportCache(load_test_id)
        self.current_execution_cache = LoadTestCurrentCache()

    @asynccontextmanager
    async def guard(self, phase_name: str, timeout: int = 10 * 60):
        context = load_test_context.get()
        try:
            async with asyncio.timeout(timeout):
                yield
        except Exception as e:
            # await self.reporter.finish_script_report_with_error(context.execution_id, e, context, phase_name)
            raise e

    async def start(self, execution_id: str):
        load_test_context.set(LoadTestExecutionContext(load_test_id=self.load_test_id, execution_id=execution_id))

        async with self.guard("Start supervisor task"):
            start_load_test_supervisor.delay(self.load_test_id, execution_id)
        async with self.guard("Get load test execution info"):
            load_test_report = await self.report_cache.get(execution_id)
            number_of_workers = await self._get_and_validate_number_of_workers(
                load_test_report.number_of_tasks, load_test_report.config_values.concurrency_within_a_single_worker
            )
        async with self.guard("Start celery tasks"):
            await LoadTestWorkerCache(self.load_test_id, execution_id).create_multi(
                {str(i): LoadTestWorkerStatusEnum.pending for i in range(number_of_workers)}
            )
            for i in range(number_of_workers):
                start_load_task.delay(load_test_id=self.load_test_id, execution_id=execution_id, worker_id=str(i))

    async def change_number_of_workers(self, execution_id: str, config_values: LoadTestConfig, number_of_tasks: int):
        load_test_context.set(LoadTestExecutionContext(load_test_id=self.load_test_id, execution_id=execution_id))
        async with self.guard("Get load test execution info"):
            workers = await LoadTestWorkerCache(self.load_test_id, execution_id).get_all()
            active_workers = {k: v for k, v in workers.items() if v != LoadTestWorkerStatusEnum.finished}
            current_number_of_workers = len(active_workers)
            number_of_workers = await self._get_and_validate_number_of_workers(
                number_of_tasks, config_values.concurrency_within_a_single_worker
            )
            if number_of_workers > current_number_of_workers:
                for i in range(number_of_workers - current_number_of_workers):
                    start_load_task.delay(
                        load_test_id=self.load_test_id,
                        execution_id=execution_id,
                        worker_id=str(current_number_of_workers + i),
                    )
            if number_of_workers < current_number_of_workers:
                async with self.guard("Send stop event for part of workers"):
                    number_to_stop = current_number_of_workers - number_of_workers
                    for worker_id in list(active_workers.keys())[-number_to_stop:]:
                        await LoadTestInternalEventChannel(
                            self.load_test_id, execution_id
                        ).send_stop_specific_worker_event(worker_id)

    async def stop(self):
        if execution_id := await self.current_execution_cache.get(self.load_test_id):
            load_test_context.set(LoadTestExecutionContext(load_test_id=self.load_test_id, execution_id=execution_id))
            async with self.guard("Send stop event for all workers"):
                await LoadTestInternalEventChannel(self.load_test_id, execution_id).send_stop_workers_event()

    @staticmethod
    async def _get_and_validate_number_of_workers(number_of_tasks: int, concurrency_within_a_single_worker: int) -> int:
        celery_capacity = await get_current_celery_capacity() - 1  # Minus one supervisor task
        requested_number_of_workers = int(number_of_tasks / concurrency_within_a_single_worker)
        number_of_workers = min(requested_number_of_workers, celery_capacity)
        if requested_number_of_workers > number_of_workers:
            raise HTTPException(
                400,
                f"The requested number of workers ({requested_number_of_workers}) "
                f"exceeds the current capacity of the launched Celery ({celery_capacity}). ",
            )
        return number_of_workers
