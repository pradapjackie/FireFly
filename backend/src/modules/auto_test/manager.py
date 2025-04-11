import asyncio
from collections import defaultdict
from contextlib import asynccontextmanager
from sys import exc_info
from traceback import format_exc, format_exception
from typing import Callable, Coroutine, Dict, List, Type

from src.cache.auto_test.test_run import TestRunCache
from src.modules.auto_test.collector import Collector
from src.modules.auto_test.contexts import (
    auto_test_context,
    auto_test_contexts,
    auto_test_current_step_list,
    test_run_context,
)
from src.modules.auto_test.reporter import Reporter
from src.modules.auto_test.test_abs import TestAbs
from src.modules.environment.env import env
from src.schemas.auto_test.auto_test import AutoTest, AutoTestContext, TestClass
from src.schemas.auto_test.auto_test_history import StageEnum, StageResult, StatusEnum
from src.schemas.auto_test.common import TestError
from src.schemas.auto_test.test_run import TestRunStatus
from src.utils.rate_limiter import Singleton


class CancelError(Exception):
    def __init__(self, message):
        super().__init__(message)


class TestManager:
    def __init__(self, run_id: str):
        self.run_id: run_id
        self.collector = Collector()
        self.reporter = Reporter(run_id)
        self.group_setup_lock = asyncio.Lock()
        self.group_teardown_lock = asyncio.Lock()
        self.tests_in_each_class_counter: Dict[TestClass, int] = {}
        self.group_setup_complete_events: Dict[TestClass, asyncio.Event] = {}
        self.group_teardown_complete_events: Dict[TestClass, asyncio.Event] = {}
        self.test_run_cache = TestRunCache(run_id)

    @asynccontextmanager
    async def guard(self, phase_name: str, timeout: int = 10 * 60):
        try:
            async with asyncio.timeout(timeout):
                yield
        except Exception as e:
            exc_type, value, _ = exc_info()
            error = TestError(
                name=f"{exc_type.__name__} during {phase_name} phase. Test Run finished.",
                message=str(e),
                traceback=format_exc(),
            )
            await self.reporter.finish_test_run_with_error(error)
            raise e from None

    async def run_tests(self):
        async with self.guard("Status change to pending"):
            await self.reporter.update_test_run_status(TestRunStatus.pending)

        async with self.guard("Context preparation"):
            test_run = await self.test_run_cache.get()
            test_run_context.set(test_run)

            env.prime_environment(
                env_name=test_run.env_name,
                setting_overwrite=test_run.setting_overwrite,
                env_user_contexts=[auto_test_context],
                env_user_multi_contexts=[auto_test_contexts],
            )

        async with self.guard("AutoTest collection"):
            selected_tests = await self.collector.collect_test_by_ids(test_run.test_ids, test_run.root_folder)

        async with self.guard("AutoTest priming with env and config"):
            self.collector.prime_tests_with_env(env, selected_tests)
            self.collector.prime_tests_with_run_config(test_run.run_config, selected_tests)

        async with self.guard("Update report"):
            await self.reporter.enrich_test_run_with_tests(selected_tests)
            await self.reporter.update_test_run_status(TestRunStatus.primed)

        async with self.guard("Prepare async tasks and events"):
            selected_classes: Dict[TestClass, List] = defaultdict(list)
            for test in selected_tests:
                selected_classes[test.test_class].append(test.id)
            self.tests_in_each_class_counter = {
                test_class: len(test_ids) for test_class, test_ids in selected_classes.items()
            }

            auto_test_contexts.set(None)

            group_setup = [self.run_group_setup(test_class, ids) for test_class, ids in selected_classes.items()]
            test_calls = [self.run_one_test(test) for test in selected_tests]
            group_teardown = [self.run_group_teardown(test_class, ids) for test_class, ids in selected_classes.items()]

            self.group_setup_complete_events = {test_class: asyncio.Event() for test_class in selected_classes}
            self.group_teardown_complete_events = {test_class: asyncio.Event() for test_class in selected_classes}

        async with self.guard("Status change to running"):
            await self.reporter.update_test_run_status(TestRunStatus.running)

        async with self.guard("Run auto tests", timeout=None):
            for task in asyncio.as_completed([*group_setup, *test_calls, *group_teardown]):
                await task

        async with self.guard("Clear run singletons"):
            Singleton.clear_by_test_run(test_run.id)

        async with self.guard("Finish test run report"):
            await self.reporter.finish_test_run_report()

    @asynccontextmanager
    async def stage(self, stage_name: StageEnum, test_contexts: List[AutoTestContext]):
        auto_test_current_step_list.set([])
        stage_result = StageResult()
        try:
            yield
        except CancelError as e:
            stage_result.status = StatusEnum.fail
            stage_result.errors.append(TestError(name="Canceled", message=str(e), traceback=""))
        except ExceptionGroup as e:
            stage_result.status = StatusEnum.fail
            stage_result.errors.extend(
                [
                    TestError(name=type(exc).__name__, message=str(exc), traceback="".join(format_exception(exc)))
                    for exc in e.exceptions
                ]
            )
        except Exception as e:
            exc_type, value, _ = exc_info()
            stage_result.status = StatusEnum.fail
            stage_result.errors.append(TestError(name=exc_type.__name__, message=str(e), traceback=format_exc()))
        else:
            stage_result.status = StatusEnum.success

        stage_result.steps_data = auto_test_current_step_list.get()
        await self.reporter.update_auto_test_stage(test_contexts, stage_name, stage_result)

    async def run_group_setup(self, test_class: TestClass, test_ids: List[str]):
        auto_test_contexts.set([AutoTestContext(id=test_id) for test_id in test_ids])
        async with self.stage(StageEnum.group_setup, auto_test_contexts.get()):
            for test_parent in test_class.cls.__mro__[::-1]:
                if issubclass(test_parent, TestAbs) and StageEnum.group_setup in test_parent.__dict__.keys():
                    await test_parent.group_setup()
        async with self.group_setup_lock:
            self.group_setup_complete_events[test_class].set()

    async def run_setup(
        self, test_class: Type[TestAbs], test_instance: TestAbs, test_context: AutoTestContext, params: Dict
    ):
        async with self.stage(StageEnum.setup, [test_context]):
            group_setup_stage = await self.reporter.auto_test_history_stages_cache.get(
                test_context.id, StageEnum.group_setup
            )
            if group_setup_stage.status == StatusEnum.fail:
                raise CancelError("Cancel due to group setup failed")
            for test_parent in test_class.__mro__[::-1]:
                if issubclass(test_parent, TestAbs) and StageEnum.setup in test_parent.__dict__.keys():
                    await test_parent.setup(test_instance, **params)

    async def run_call(self, test_instance: TestAbs, test_context: AutoTestContext, method_name: str, params: Dict):
        async with self.stage(StageEnum.call, [test_context]):
            group_setup_stage = await self.reporter.auto_test_history_stages_cache.get(
                test_context.id, StageEnum.group_setup
            )
            setup_stage = await self.reporter.auto_test_history_stages_cache.get(test_context.id, StageEnum.setup)
            if group_setup_stage.status == StatusEnum.fail:
                raise CancelError("Cancel due to group setup failed")
            if setup_stage.status == StatusEnum.fail:
                raise CancelError("Cancel due to setup failed")
            await getattr(test_instance, method_name)(**params)

    async def run_teardown(
        self, test_class: Type[TestAbs], test_instance: TestAbs, test_context: AutoTestContext, params: Dict
    ):
        async with self.stage(StageEnum.teardown, [test_context]):
            group_setup_stage = await self.reporter.auto_test_history_stages_cache.get(
                test_context.id, StageEnum.group_setup
            )
            if group_setup_stage.status == StatusEnum.fail:
                raise CancelError("Cancel due to group setup failed")
            for test_parent in test_class.__mro__:
                if issubclass(test_parent, TestAbs) and StageEnum.teardown in test_parent.__dict__.keys():
                    await test_parent.teardown(test_instance, **params)

    async def run_group_teardown(self, test_class: TestClass, test_ids: List[str]):
        await self.group_teardown_complete_events[test_class].wait()
        auto_test_contexts.set([AutoTestContext(id=test_id) for test_id in test_ids])
        async with self.stage(StageEnum.group_teardown, auto_test_contexts.get()):
            for test_parent in test_class.cls.__mro__[::-1]:
                if issubclass(test_parent, TestAbs) and StageEnum.group_teardown in test_parent.__dict__.keys():
                    await test_parent.group_teardown()

    async def _run_one_test(self, auto_test: AutoTest):
        test_instance = auto_test.test_class.cls()
        auto_test_context.set(AutoTestContext(id=auto_test.id))

        await self.run_setup(auto_test.test_class.cls, test_instance, auto_test_context.get(), auto_test.params)
        await self.run_call(test_instance, auto_test_context.get(), auto_test.test_method.name, auto_test.params)
        await self.run_teardown(auto_test.test_class.cls, test_instance, auto_test_context.get(), auto_test.params)

    async def run_one_test(self, auto_test: AutoTest):
        await self.group_setup_complete_events[auto_test.test_class].wait()

        if auto_test.run_in_separate_thread:
            await self.run_in_separate_thread(self._run_one_test, auto_test)
        else:
            await self._run_one_test(auto_test)

        self.tests_in_each_class_counter[auto_test.test_class] -= 1
        if self.tests_in_each_class_counter[auto_test.test_class] == 0:
            async with self.group_teardown_lock:
                self.group_teardown_complete_events[auto_test.test_class].set()

    def run_all_sync(self) -> None:
        asyncio.get_event_loop().run_until_complete(self.run_tests())

    @staticmethod
    def _run_in_new_loop(coro: Callable, *args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            coro = coro(*args, **kwargs)
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    async def run_in_separate_thread(self, coro: Callable, *args, **kwargs) -> Coroutine:
        return await asyncio.to_thread(self._run_in_new_loop, coro, *args, **kwargs)
