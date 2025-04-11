import asyncio
from typing import List

from src.cache.base import CacheBase
from src.schemas.auto_test.auto_test_history import AutoTestHistory, AutoTestHistoryUpdate


class AutoTestHistoryCache(CacheBase[AutoTestHistory, AutoTestHistoryUpdate]):
    def __init__(self, run_id: str):
        self.run_id = run_id
        super().__init__(AutoTestHistory)

    async def create(self, data: AutoTestHistory):
        await self._save_model(f"{self.run_id}:autotest:{data.test_id}", data)

    async def get(self, test_id: str) -> AutoTestHistory | None:
        return await self._get_model(f"{self.run_id}:autotest:{test_id}")

    async def get_multi(self, test_ids: List[str]) -> List[AutoTestHistory]:
        return await asyncio.gather(*[self.get(test_id) for test_id in test_ids])

    async def update(self, test_id: str, data: AutoTestHistoryUpdate):
        return await self._update_model(f"{self.run_id}:autotest:{test_id}", data)
