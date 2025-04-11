from src.cache.base import CacheBase
from src.schemas.script_runner.script_history import ScriptHistory, ScriptHistoryUpdate


class ScriptHistoryCache(CacheBase[ScriptHistory, ScriptHistoryUpdate]):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(ScriptHistory)

    async def create(self, execution_id: str, data: ScriptHistory):
        await self._save_model(f"script:{self.script_id}:{execution_id}:data", data)

    async def get(self, execution_id: str) -> ScriptHistory | None:
        return await self._get_model(f"script:{self.script_id}:{execution_id}:data")

    async def update(self, execution_id: str, data: ScriptHistoryUpdate):
        return await self._update_model(f"script:{self.script_id}:{execution_id}:data", data)
