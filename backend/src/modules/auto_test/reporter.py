import asyncio
from datetime import datetime, timezone
from typing import Dict, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.cache import AutoTestHistoryCache, AutoTestHistoryGroupsCache, AutoTestHistoryStagesCache, AutoTestTagsCache
from src.cache.auto_test.pending_runs import PendingRunsCache
from src.cache.auto_test.test_run import TestRunCache, TestRunChannel
from src.core.config import settings as app_settings
from src.db.session import SessionLocal
from src.schemas import User
from src.schemas.auto_test.auto_test import AutoTest, AutoTestContext
from src.schemas.auto_test.auto_test_history import (
    AutoTestGroup,
    AutoTestHistory,
    AutoTestHistoryDB,
    AutoTestHistoryUpdate,
    AutoTestItem,
    AutoTestStages,
    AutoTestStatisticResponse,
    ResultTreeStatus,
    StageEnum,
    StageResult,
    StatusEnum,
    TestResultTree,
)
from src.schemas.auto_test.common import TestError
from src.schemas.auto_test.test_run import (
    StartTestRunRequest,
    StartTestRunResponse,
    TestRun,
    TestRunDB,
    TestRunListResponse,
    TestRunStatisticResponse,
    TestRunStatus,
    TestRunUpdate,
)
from src.schemas.environment import EnvEnum
from src.utils.async_iterator_utils import batch
from src.utils.format import format_class_name, format_method_name


class Reporter:
    def __init__(self, run_id: str | None = None):
        self.run_id = run_id
        self.db_session = SessionLocal
        self.pending_runs_cache = PendingRunsCache()
        self.auto_test_tags_cache = AutoTestTagsCache()
        if self.run_id:
            self.test_run_cache = TestRunCache(run_id)
            self.auto_test_history_cache = AutoTestHistoryCache(run_id)
            self.auto_test_history_groups_cache = AutoTestHistoryGroupsCache(run_id)
            self.auto_test_history_stages_cache = AutoTestHistoryStagesCache(run_id)
            self.test_run_channel = TestRunChannel(run_id)

    async def start_test_run_report(self, user: User, start_request: StartTestRunRequest) -> StartTestRunResponse:
        start_time = datetime.now(timezone.utc)
        test_ids_by_tags = await self.auto_test_tags_cache.get_by_tags(start_request.tags, start_request.root_folder)
        start_request.test_ids.extend(test_ids_by_tags)
        test_run = TestRun(
            id=self.run_id,
            user=user,
            start_time=start_time,
            version=app_settings.PROJECT_VERSION,
            **start_request.model_dump(),
        )
        await self.test_run_cache.create(test_run)
        await self.pending_runs_cache.add(start_request.root_folder, start_request.env_name, self.run_id)
        return StartTestRunResponse(**test_run.model_dump())

    async def update_test_run_status(self, status: TestRunStatus):
        await self.test_run_cache.update(TestRunUpdate(status=status))
        await self.test_run_channel.update(status)

    async def finish_test_run_with_error(self, error: TestError):
        test_run = await self.test_run_cache.get()
        await self.update_test_run_status(status=TestRunStatus.fail)
        await self.test_run_cache.update(TestRunUpdate(error=error))
        await self.pending_runs_cache.remove(test_run.root_folder, test_run.env_name, self.run_id)

    async def get_test_run_statistic(self) -> TestRun:
        return await self.test_run_cache.get()

    async def get_test_run_status(self) -> TestRunStatus:
        return await self.test_run_cache.get_status()

    async def enrich_test_run_with_tests(self, auto_tests: List[AutoTest]):
        all_groups: Dict[str, AutoTestGroup] = {}
        for auto_test in auto_tests:
            auto_test_groups = self._calc_test_groups_and_update_test_run_groups(auto_test, all_groups)
            history = AutoTestHistory(
                test_id=auto_test.id,
                iteration_name=auto_test.iteration_name,
                method_name=auto_test.test_method.name,
                description=auto_test.test_method.description,
                test_run_id=self.run_id,
                params=auto_test.params,
                run_config=auto_test.run_config,
                groups=auto_test_groups,
            )
            await self.auto_test_history_cache.create(history)
            await self.auto_test_history_stages_cache.create_multi(auto_test.id, AutoTestStages())
        await self.auto_test_history_groups_cache.create_multi(all_groups)
        await self.test_run_cache.update(TestRunUpdate(group_ids=list(all_groups.keys())))
        await self.test_run_cache.increment_by(StatusEnum.pending, len(auto_tests))

    async def get_test_run_tree(self) -> TestResultTree:
        test_run = await self.test_run_cache.get()
        if test_run.status in (TestRunStatus.idle, TestRunStatus.pending):
            return TestResultTree(status=ResultTreeStatus.idle)
        elif test_run.status == TestRunStatus.fail:
            return TestResultTree(status=ResultTreeStatus.failed)
        else:
            groups = await self.auto_test_history_groups_cache.get_multi(test_run.group_ids)
            auto_tests_history = await self.auto_test_history_cache.get_multi(test_run.test_ids)
            first_level, group_map = [], {}
            for group in groups:
                group.root and first_level.append(group.name)
                group_map[group.id] = group
            items_map = {
                history.test_id: AutoTestItem(name=history.iteration_name, status=history.status)
                for history in auto_tests_history
            }
            tree_status = (
                ResultTreeStatus.finished if test_run.status == TestRunStatus.success else ResultTreeStatus.pending
            )
            return TestResultTree(status=tree_status, first_level=first_level, groups=group_map, items=items_map)

    async def get_test_run_item(self, auto_test_id: str) -> AutoTestHistory | None:
        item = await self.auto_test_history_cache.get(auto_test_id)
        if not item:
            return None
        stages = await self.auto_test_history_stages_cache.get_all(auto_test_id)
        item.stages = stages
        item.method_name = format_method_name(item.method_name)
        return item

    async def get_test_run_items(self, auto_test_ids: List[str]) -> List[AutoTestHistory]:
        return await asyncio.gather(*[self.get_test_run_item(test_id) for test_id in auto_test_ids])

    async def update_auto_test_stage(
        self, test_contexts: List[AutoTestContext], stage_name: StageEnum, stage_result: StageResult
    ):
        for test_context in test_contexts:
            test_id = test_context.id
            await self.auto_test_history_stages_cache.update(test_id, stage_name, stage_result)
            auto_test_history_current = await self.auto_test_history_cache.get(test_id)
            auto_test_history_update = AutoTestHistoryUpdate()

            if stage_result.errors:
                auto_test_history_update.errors = auto_test_history_current.errors | {stage_name: stage_result.errors}

            auto_test_history_update.env_used = auto_test_history_current.env_used | test_context.env_used
            auto_test_history_update.generated_params = (
                auto_test_history_current.generated_params | test_context.generated_params
            )
            auto_test_history_update.assets_path = auto_test_history_current.assets_path | test_context.assets_path
            auto_test_history_update.warnings = auto_test_history_current.warnings + test_context.warnings
            test_context.warnings = []

            test_not_failed = auto_test_history_current.status != StatusEnum.fail
            stage_is_failed = stage_result.status == StatusEnum.fail
            stage_is_successful = stage_result.status == StatusEnum.success

            change_to_fail = test_not_failed and stage_is_failed
            change_to_success = test_not_failed and stage_name == StageEnum.teardown and stage_is_successful

            if change_to_fail or change_to_success:
                auto_test_history_update.status = stage_result.status
                for group_name in auto_test_history_current.groups:
                    await self.auto_test_history_groups_cache.increment_by(group_name, stage_result.status, 1)
                    await self.auto_test_history_groups_cache.increment_by(
                        group_name, auto_test_history_current.status, -1
                    )
                await self.test_run_cache.increment_by(stage_result.status, 1)
                await self.test_run_cache.increment_by(auto_test_history_current.status, -1)

            await self.auto_test_history_cache.update(test_id, auto_test_history_update)

    async def finish_test_run_report(self):
        await self.update_test_run_status(status=TestRunStatus.success)
        test_run = await self.test_run_cache.get()

        test_run_db = TestRunDB(
            id=test_run.id,
            user_id=test_run.user.id,
            version=test_run.version,
            status=test_run.status,
            result_by_status=test_run.result_by_status,
            error=test_run.error,
            start_time=test_run.start_time,
            root_folder=test_run.root_folder,
            environment=test_run.env_name,
            run_config=test_run.run_config,
            group_ids=test_run.group_ids,
        )
        try:
            async with self.db_session() as db:
                await crud.test_run_history.create(db, obj_in=test_run_db)
                for chunk in batch(test_run.test_ids, 5):
                    auto_test_history_chunk = await self.get_test_run_items(chunk)
                    objects_in = [AutoTestHistoryDB(**history.model_dump()) for history in auto_test_history_chunk]
                    await crud.auto_test_history.create_multi(db, objects_in=objects_in)
        except Exception as e:
            print(f"Exception during saving report in db: {e}")
        await self.pending_runs_cache.remove(test_run.root_folder, test_run.env_name, self.run_id)

    @staticmethod
    def _calc_test_groups_and_update_test_run_groups(
        auto_test: AutoTest, all_groups: Dict[str, AutoTestGroup]
    ) -> List[str]:
        auto_test_groups = []
        class_name = format_class_name(auto_test.test_class.name)
        method_name = format_method_name(auto_test.test_method.name)
        full_path_parts = f"{auto_test.filepath}.{class_name}.{method_name}".split(".")
        prev_group = None
        for i in range(1, len(full_path_parts) + 1):
            group_id = ".".join(full_path_parts[0:i])
            group_name = full_path_parts[i - 1]
            auto_test_groups.append(group_id)
            if not prev_group:
                if not all_groups.get(group_id):
                    all_groups[group_id] = AutoTestGroup(id=group_id, name=group_name, root=True)
            else:
                if not all_groups.get(group_id):
                    all_groups[group_id] = AutoTestGroup(id=group_id, name=group_name)
                all_groups[prev_group].groups.add(group_id)

                if i == len(full_path_parts):
                    all_groups[group_id].auto_tests.add(auto_test.id)

            prev_group = group_id
            all_groups[group_id].result_by_status.increment(StatusEnum.pending)
        return auto_test_groups

    async def get_pending_test_runs(self, root_folder: str, env: EnvEnum) -> List[TestRun]:
        pending_run_ids = await self.pending_runs_cache.get(root_folder, env)
        return [await TestRunCache(run_id).get() for run_id in pending_run_ids]

    async def _get_test_runs(self, db: AsyncSession, root_folder: str, env: EnvEnum, n=20) -> List[TestRun]:
        test_runs = await self.get_pending_test_runs(root_folder, env)
        if len(test_runs) < n:
            test_runs.extend(await crud.test_run_history.get_runs(db, root_folder, env, n=n - len(test_runs)))
        return test_runs

    async def get_test_runs(self, db: AsyncSession, root_folder: str, env: EnvEnum) -> TestRunListResponse:
        test_runs = await self._get_test_runs(db, root_folder, env)
        test_runs_map = {test_run.id: test_run for test_run in test_runs}
        return TestRunListResponse(ids=list(test_runs_map.keys()), runs=test_runs_map)

    async def get_auto_tests_statistic(
        self, db: AsyncSession, root_folder: str, env: EnvEnum
    ) -> TestRunStatisticResponse:
        stat = await crud.auto_test_history.get_stat(db, root_folder, env)
        test_runs = await self._get_test_runs(db, root_folder, env)
        return TestRunStatisticResponse(stat=stat, test_runs=test_runs)

    @staticmethod
    async def get_one_auto_test_statistic(db: AsyncSession, test_id) -> AutoTestStatisticResponse:
        auto_test = await crud.auto_test.get(db, id=test_id)
        statistic = await crud.auto_test_history.get_auto_tests_for_statistic(db, test_id, limit=10)
        result_by_status = await crud.auto_test_history.get_auto_test_statistic(db, test_id, limit=10)

        return AutoTestStatisticResponse(
            full_name=f"{auto_test.class_name} : {auto_test.method_name} : {auto_test.iteration_name}",
            result_by_status=result_by_status,
            statistic=statistic,
        )

    async def update_test_report_after_finish(
        self, run_id: str, auto_test_id: str, history_update: AutoTestHistoryUpdate
    ):
        await self.auto_test_history_cache.update(auto_test_id, history_update)
        try:
            async with self.db_session() as db:
                current = await crud.auto_test_history.get_one_test_history(db, run_id, auto_test_id)
                history_update = jsonable_encoder(history_update.model_dump(exclude_unset=True))
                await crud.auto_test_history.update(db, db_obj=current, obj_in=history_update)
        except Exception as e:
            print(e)
