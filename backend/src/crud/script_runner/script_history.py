from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.crud.base import CRUDBase
from src.schemas.script_runner.script_history import ScriptHistoryDB


class CRUDScriptHistory(CRUDBase[models.ScriptHistory, ScriptHistoryDB, ScriptHistoryDB]):
    async def clear_history(self, db: AsyncSession):
        await self.delete_all(db)


script_history = CRUDScriptHistory(models.ScriptHistory)
