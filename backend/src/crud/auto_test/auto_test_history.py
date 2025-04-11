from typing import List

from pytz import utc
from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from src import models
from src.crud.base import CRUDBase
from src.schemas.auto_test.auto_test_history import AutoTestHistoryDB, AutoTestStatistic
from src.schemas.auto_test.common import ResultByStatus
from src.schemas.environment import EnvEnum


class CRUDAutoTestHistory(CRUDBase[models.AutoTestHistory, AutoTestHistoryDB, AutoTestHistoryDB]):
    async def get_stat(self, db: AsyncSession, root_folder: str, env: EnvEnum) -> ResultByStatus:
        query_result = await db.execute(
            select(self.model.status, func.count())
            .join(models.TestRunHistory)
            .where(
                models.TestRunHistory.root_folder == root_folder,
                models.TestRunHistory.environment == env,
            )
            .group_by(self.model.status)
            .limit(20)
        )
        result_by_status = ResultByStatus()
        for status, count in query_result:
            result_by_status.increment_by(status, count)
        return result_by_status

    async def get_auto_tests_for_statistic(self, db: AsyncSession, test_id: str, limit=10) -> List[AutoTestStatistic]:
        query_result = await db.execute(
            select(
                models.TestRunHistory.start_time,
                self.model.status,
            )
            .join(models.TestRunHistory)
            .where(self.model.test_id == test_id)
            .order_by(desc(models.TestRunHistory.start_time))
            .limit(limit)
        )
        result = []
        for date, status in query_result:
            result.append(AutoTestStatistic(date=date.astimezone(utc), status=status))
        return result

    async def get_auto_test_statistic(self, db: AsyncSession, test_id: str, limit=10) -> ResultByStatus:
        query_result = await db.execute(
            select(self.model.status, func.count())
            .where(self.model.test_id == test_id)
            .group_by(self.model.status)
            .limit(limit)
        )
        result_by_status = ResultByStatus()
        for status, count in query_result:
            result_by_status.increment_by(status, count)
        return result_by_status

    async def clear_history(self, db: AsyncSession):
        await db.execute(delete(self.model))

    async def get_one_test_history(
        self, db: AsyncSession, test_run_id: str, test_id: str
    ) -> models.AutoTestHistory | None:
        result = await db.execute(
            select(self.model).where(self.model.test_run_id == test_run_id, self.model.test_id == test_id)
        )
        return result.scalars().first()


auto_test_history = CRUDAutoTestHistory(models.AutoTestHistory)
