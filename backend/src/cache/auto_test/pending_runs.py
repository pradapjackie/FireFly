from typing import List

from src.cache.base import CacheBase
from src.modules.auto_test.config import settings
from src.schemas.environment import EnvEnum


class PendingRunsCache(CacheBase[List, List]):
    async def add(self, root_folder: str, env_name: EnvEnum, *values: str):
        await self._add_to_list(f"{settings.AUTO_TEST_PENDING_RUNS}_{root_folder}_{env_name}", *values)

    async def remove(self, root_folder: str, env_name: EnvEnum, value: str):
        await self._remove_from_list(f"{settings.AUTO_TEST_PENDING_RUNS}_{root_folder}_{env_name}", value)

    async def get(self, root_folder: str, env_name: EnvEnum) -> List[str]:
        return await self._get_list(f"{settings.AUTO_TEST_PENDING_RUNS}_{root_folder}_{env_name}") or []
