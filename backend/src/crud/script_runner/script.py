from typing import List, Tuple

from fastapi.encoders import jsonable_encoder
from pytz import utc
from sqlalchemy import desc, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.core.config import settings
from src.crud.base import CRUDBase
from src.schemas.script_runner.script import ScriptDB
from src.schemas.script_runner.script_history import ScriptError, ScriptHistoryDisplay, ScriptHistoryItem, ScriptResult


class CRUDScript(CRUDBase[models.Script, ScriptDB, ScriptDB]):
    @staticmethod
    def version_tuple(v: str) -> Tuple[int, ...]:
        return tuple(map(int, (v.split("."))))

    async def save_scripts(self, db: AsyncSession, scripts: List[ScriptDB]) -> None:
        for script_item in scripts:
            query = (
                insert(self.model)
                .values(**jsonable_encoder(script_item))
                .on_duplicate_key_update(
                    supported_to=settings.PROJECT_VERSION,
                    params=jsonable_encoder(script_item.params),
                    description=jsonable_encoder(script_item.description),
                )
            )
            await db.execute(query)
        await db.commit()

    async def clear(self, db: AsyncSession):
        await self.delete_all(db)

    async def get_scripts(self, db: AsyncSession, root_folder: str) -> List[models.Script]:
        result = await db.execute(select(self.model).where(models.Script.root_folder == root_folder))
        scripts = result.scalars().all()
        return [
            script_item
            for script_item in scripts
            if self.version_tuple(script_item.supported_from)
            <= self.version_tuple(settings.PROJECT_VERSION)
            <= self.version_tuple(script_item.supported_to)
        ]

    async def get_script_history(self, db: AsyncSession, script_id: str, limit=20) -> ScriptHistoryDisplay:
        query_result = await db.execute(
            select(self.model.display_name, models.ScriptHistory, models.User.full_name)
            .select_from(self.model)
            .join(models.ScriptHistory, self.model.id == models.ScriptHistory.script_id, isouter=True)
            .join(models.User, models.ScriptHistory.user_id == models.User.id, isouter=True)
            .where(self.model.id == script_id)
            .order_by(desc(models.ScriptHistory.start_time))
            .limit(limit)
        )
        result = None
        for script_display_name, history, user_display_name in query_result:
            if not result:
                result = ScriptHistoryDisplay(name=script_display_name, history=[])
            if history:
                result.history.append(
                    ScriptHistoryItem(
                        execution_id=history.id,
                        environment=history.environment,
                        status=history.status,
                        result=ScriptResult(type=history.result_type, object=history.result)
                        if history.result_type
                        else None,
                        errors=[ScriptError(**item) for item in history.errors] if history.errors else None,
                        params=history.params,
                        env_used=history.env_used,
                        user_name=user_display_name,
                        start_time=history.start_time.astimezone(utc),
                        end_time=history.end_time.astimezone(utc),
                    )
                )
        return result


script = CRUDScript(models.Script)
