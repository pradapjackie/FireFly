import asyncio
from typing import Dict, List

from src.cache.base import CacheBase
from src.schemas.auto_test.auto_test_history import AutoTestGroup
from src.schemas.auto_test.common import ResultByStatus


class AutoTestHistoryGroupsCache(CacheBase[AutoTestGroup, AutoTestGroup]):
    def __init__(self, run_id: str):
        self.run_id = run_id
        super().__init__(AutoTestGroup)

    async def create(self, group_id: str, group: AutoTestGroup):
        group = group.model_copy()
        result_by_status = group.result_by_status.model_dump()
        group.result_by_status = None
        group_dict = self.converter.encode_to_dict(group)
        await self._save_dict(f"{self.run_id}:groups:{group_id}:info", group_dict)
        await self._save_dict(f"{self.run_id}:groups:{group_id}:result", result_by_status)

    async def get(self, group_name: str) -> AutoTestGroup:
        group = await self._get_model(f"{self.run_id}:groups:{group_name}:info")
        result_by_status = await self._get_decoded_dict(f"{self.run_id}:groups:{group_name}:result")
        group.result_by_status = ResultByStatus(**result_by_status)
        return group

    async def create_multi(self, data: Dict[str, AutoTestGroup]):
        await asyncio.gather(*[self.create(group_id, group) for group_id, group in data.items()])

    async def get_multi(self, groups: List[str]) -> List[AutoTestGroup]:
        return await asyncio.gather(*[self.get(group_name) for group_name in groups])

    async def increment_by(self, group_name: str, status_name: str, value: int):
        await self._increment_value_in_dict(f"{self.run_id}:groups:{group_name}:result", status_name, value)
