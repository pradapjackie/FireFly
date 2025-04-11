from typing import List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.crud.base import CRUDBase
from src.schemas.environment import AutoTestEnv, AutoTestEnvUpdate, EnvEnum


class CRUDAutoTestEnv(CRUDBase[models.AutoTestEnvironment, AutoTestEnv, AutoTestEnvUpdate]):
    async def get_env_params(self, db: AsyncSession, env_name: EnvEnum) -> List[AutoTestEnv]:
        query_result = await db.execute(select(self.model).where(models.AutoTestEnvironment.env == env_name.value))
        return [AutoTestEnv.model_validate(param) for param in query_result.scalars().all()]

    async def remove_env_param(self, db: AsyncSession, env_name: EnvEnum, param: str):
        await db.execute(
            delete(self.model).where(models.AutoTestEnvironment.env == env_name.value, self.model.param == param)
        )
        await db.commit()

    async def update_env_param(self, db: AsyncSession, obj_in: AutoTestEnvUpdate):
        result = await db.execute(
            select(self.model).where(
                models.AutoTestEnvironment.env == obj_in.env.value, self.model.param == obj_in.param
            )
        )
        await self.update(db, db_obj=result.scalars().first(), obj_in=obj_in)


auto_test_env = CRUDAutoTestEnv(models.AutoTestEnvironment)
