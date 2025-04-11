from typing import List, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.core.config import settings
from src.crud.base import CRUDBase
from src.schemas.auto_test.auto_test import AutoTestDB


class CRUDAutoTest(CRUDBase[models.AutoTest, AutoTestDB, AutoTestDB]):
    @staticmethod
    def version_tuple(v: str) -> Tuple[int, ...]:
        return tuple(map(int, (v.split("."))))

    async def add_auto_tests(self, db: AsyncSession, auto_tests: List[AutoTestDB]) -> None:
        for autotest in auto_tests:
            query = (
                insert(self.model)
                .values(**jsonable_encoder(autotest))
                .on_duplicate_key_update(
                    supported_to=settings.PROJECT_VERSION,
                    params=jsonable_encoder(autotest.params),
                    description=jsonable_encoder(autotest.description),
                    required_run_config=jsonable_encoder(autotest.required_run_config),
                )
            )
            await db.execute(query)
        await db.commit()

    async def get_auto_tests(self, db: AsyncSession, root_folder: str) -> List[models.AutoTest]:
        result = await db.execute(select(self.model).where(models.AutoTest.root_folder == root_folder))
        tests = result.scalars().all()
        return [
            test
            for test in tests
            if self.version_tuple(test.supported_from)
            <= self.version_tuple(settings.PROJECT_VERSION)
            <= self.version_tuple(test.supported_to)
        ]

    async def clear(self, db: AsyncSession):
        await db.execute(delete(self.model))


auto_test = CRUDAutoTest(models.AutoTest)
