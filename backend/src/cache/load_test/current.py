from typing import Dict

from src.cache.base import CacheBase


class LoadTestCurrentCache(CacheBase[Dict, Dict]):
    def __init__(self):
        self.key = f"load_test:current"
        super().__init__()

    async def save(self, load_test_id: str, execution_id: str):
        await self._update_key_value_in_dict(self.key, load_test_id, execution_id)

    async def get(self, load_test_id: str) -> str | None:
        result = await self._get_values_from_dict(self.key, [load_test_id])
        return result[0] if result else None

    async def remove(self, load_test_id: str):
        await self._delete_keys_from_dict(self.key, [load_test_id])
