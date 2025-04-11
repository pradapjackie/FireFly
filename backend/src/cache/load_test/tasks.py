import json
from collections import Counter
from typing import Any, Dict

from src.cache.base import CacheBase
from src.cache.load_test.internal_event_channel import LoadTestInternalEventChannel
from src.schemas.load_test.load_test_history import LoadTestTaskStatusEnum, LoadTestTaskStatusHistory


class LoadTestTaskCache(CacheBase[Any, Any]):
    def __init__(self, load_test_id: str, execution_id: str):
        self.load_test_id = load_test_id
        self.execution_id = execution_id
        self.internal_channel = LoadTestInternalEventChannel(load_test_id, execution_id)
        self.key_prefix = f"load_test:{self.load_test_id}:{execution_id}:tasks"
        super().__init__()

    async def create_multi(self, tasks_with_status: Dict[str, LoadTestTaskStatusEnum]):
        count_by_status: Dict[LoadTestTaskStatusEnum, int] = dict(Counter(tasks_with_status.values()))
        await self._save_dict(f"{self.key_prefix}:current", tasks_with_status)
        for status, count in count_by_status.items():
            await self._increment_value_in_dict(f"{self.key_prefix}:status_map", status, count)
        await self.internal_channel.start_task_updates()

    async def update_status(self, task_id: str, new_status: LoadTestTaskStatusEnum):
        old_status = LoadTestTaskStatusEnum(await self._get_value_from_dict(f"{self.key_prefix}:current", task_id))
        await self._update_key_value_in_dict(f"{self.key_prefix}:current", task_id, new_status)
        await self._increment_value_in_dict(f"{self.key_prefix}:status_map", old_status, -1)
        await self._increment_value_in_dict(f"{self.key_prefix}:status_map", new_status, 1)

    async def get_current_status_map(self) -> Dict[str, int]:
        return await self._get_decoded_dict(f"{self.key_prefix}:status_map")

    async def add_status_history(self, time_string: str, data: LoadTestTaskStatusHistory):
        await self._update_key_value_in_dict(
            f"{self.key_prefix}:status_map_history", time_string, data.model_dump_json()
        )

    async def get_status_history(self) -> Dict[str, LoadTestTaskStatusHistory]:
        status_history = await self._get_decoded_dict(f"{self.key_prefix}:status_map_history")
        return {
            time_string: LoadTestTaskStatusHistory.model_validate_json(item)
            for time_string, item in status_history.items()
        }
