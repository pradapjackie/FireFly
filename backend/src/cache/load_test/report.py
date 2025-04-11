from src.cache.base import CacheBase
from src.schemas.load_test.load_test_history import LoadTestHistory, LoadTestHistoryUpdate


class LoadTestReportCache(CacheBase[LoadTestHistory, LoadTestHistoryUpdate]):
    def __init__(self, load_test_id: str):
        self.load_test_id = load_test_id
        super().__init__(LoadTestHistory)

    async def create(self, execution_id: str, data: LoadTestHistory):
        await self._save_model(f"load_test:{self.load_test_id}:{execution_id}:data", data)

    async def get(self, execution_id: str) -> LoadTestHistory | None:
        return await self._get_model(f"load_test:{self.load_test_id}:{execution_id}:data")

    async def update(self, execution_id: str, data: LoadTestHistoryUpdate):
        return await self._update_model(f"load_test:{self.load_test_id}:{execution_id}:data", data)
