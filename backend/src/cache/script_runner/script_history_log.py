from typing import Dict, List

from src.cache.base import CacheBase


class ScriptHistoryLogCache(CacheBase[List, List]):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(None)

    async def add(self, execution_id: str, message: str) -> int:
        return await self._add_to_list(f"script:{self.script_id}:{execution_id}:log", message)

    async def get(self, execution_id: str) -> Dict[int, str]:
        return await self._get_enumerate_list(f"script:{self.script_id}:{execution_id}:log")
