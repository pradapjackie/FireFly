import asyncio
from typing import Dict

from src.cache.base import CacheBase
from src.cache.load_test.internal_event_channel import LoadTestInternalEventChannel
from src.schemas.load_test.load_test_history import LoadTestWorkerStatusEnum


class LoadTestWorkerCache(CacheBase[str, str]):
    def __init__(self, load_test_id: str, execution_id: str):
        self.load_test_id = load_test_id
        self.execution_id = execution_id
        self.internal_channel = LoadTestInternalEventChannel(load_test_id, execution_id)
        self.key = f"load_test:{self.load_test_id}:{execution_id}:workers"
        super().__init__()

    async def create_multi(self, workers_with_status: Dict[str, LoadTestWorkerStatusEnum]):
        await self._save_dict(self.key, workers_with_status)
        await asyncio.gather(
            *[
                self.internal_channel.update_worker_status(worker_id, status)
                for worker_id, status in workers_with_status.items()
            ]
        )

    async def update_status(self, worker_id: str, new_status: LoadTestWorkerStatusEnum):
        await self._update_key_value_in_dict(self.key, worker_id, new_status)
        await self.internal_channel.update_worker_status(worker_id, new_status)

    async def get(self, worker_id) -> LoadTestWorkerStatusEnum:
        return LoadTestWorkerStatusEnum(await self._get_value_from_dict(self.key, worker_id))

    async def get_all(self) -> Dict[str, LoadTestWorkerStatusEnum]:
        result = await self._get_dict(self.key)
        return {k.decode("UTF-8"): LoadTestWorkerStatusEnum(v.decode("UTF-8")) for k, v in result.items()}
