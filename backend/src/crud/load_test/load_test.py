from typing import List, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.core.config import settings
from src.crud.base import CRUDBase
from src.schemas.load_test.load_test import LoadTestDB


class CRUDLoadTest(CRUDBase[models.LoadTest, LoadTestDB, LoadTestDB]):
    @staticmethod
    def version_tuple(v: str) -> Tuple[int, ...]:
        return tuple(map(int, (v.split("."))))

    async def save_load_tests(self, db: AsyncSession, load_tests: List[LoadTestDB]) -> None:
        for test in load_tests:
            query = (
                insert(self.model)
                .values(**jsonable_encoder(test))
                .on_duplicate_key_update(
                    supported_to=settings.PROJECT_VERSION,
                    params=jsonable_encoder(test.params),
                    description=jsonable_encoder(test.description),
                )
            )
            await db.execute(query)
        await db.commit()

    async def get_load_tests(self, db: AsyncSession, root_folder: str) -> List[models.LoadTest]:
        result = await db.execute(select(self.model).where(models.LoadTest.root_folder == root_folder))
        load_tests = result.scalars().all()
        return [
            load_test_item
            for load_test_item in load_tests
            if self.version_tuple(load_test_item.supported_from)
            <= self.version_tuple(settings.PROJECT_VERSION)
            <= self.version_tuple(load_test_item.supported_to)
        ]

    async def clear(self, db: AsyncSession):
        await self.delete_all(db)


load_test = CRUDLoadTest(models.LoadTest)
