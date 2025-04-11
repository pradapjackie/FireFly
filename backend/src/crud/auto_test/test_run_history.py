from typing import List

from pytz import utc
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.crud.base import CRUDBase
from src.schemas.auto_test.test_run import TestRun, TestRunDB
from src.schemas.environment import EnvEnum


class CRUDTestRunHistory(CRUDBase[models.TestRunHistory, TestRunDB, TestRunDB]):
    async def get_runs(self, db: AsyncSession, root_folder: str, env: EnvEnum, n: int) -> List[TestRun]:
        query_result = await db.execute(
            select(self.model, models.User, func.group_concat(models.AutoTestHistory.test_id.distinct()))
            .join(models.User)
            .join(models.AutoTestHistory)
            .where(self.model.root_folder == root_folder, self.model.environment == env)
            .group_by(self.model.id)
            .order_by(desc(self.model.start_time))
            .limit(n)
        )
        result = []
        for run_history_db, user, test_id in query_result:
            result.append(
                TestRun(
                    id=run_history_db.id,
                    root_folder=run_history_db.root_folder,
                    env_name=run_history_db.environment,
                    test_ids=test_id.split(","),
                    setting_overwrite={},
                    run_config=run_history_db.run_config,
                    user=user,
                    version=run_history_db.version,
                    status=run_history_db.status,
                    result_by_status=run_history_db.result_by_status,
                    error=run_history_db.error,
                    group_ids=run_history_db.group_ids,
                    start_time=run_history_db.start_time.astimezone(utc),
                )
            )
        return result


test_run_history = CRUDTestRunHistory(models.TestRunHistory)
