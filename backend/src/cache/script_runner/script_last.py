from typing import Dict

from src.cache.base import CacheBase


class ScriptLastCache(CacheBase[Dict, Dict]):
    def __init__(self):
        self.key = f"script:last"
        super().__init__()

    async def save(self, script_id: str, execution_id: str):
        await self._update_key_value_in_dict(self.key, script_id, execution_id)

    async def get(self, script_id: str) -> str | None:
        result = await self._get_values_from_dict(self.key, [script_id])
        return result[0] if result else None
