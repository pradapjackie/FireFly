import asyncio
import json
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import Dict, List, Tuple

from src.cache.base import CacheBase
from src.core.config import settings
from src.schemas.common import CollectedObject


class BasePathsCache(CacheBase[Dict, Dict]):
    def __init__(self, module_name: str):
        self.root_key = f"collected_{module_name}_path_{settings.PROJECT_VERSION}"
        self.root_key_folders = f"collected_{module_name}_folders_path_{settings.PROJECT_VERSION}"
        super().__init__()

    async def save_paths(self, objects: List[CollectedObject]):
        sorted_objects = sorted(objects, key=lambda x: x.root_folder)
        objects_by_root_folder: Dict[str, List[CollectedObject]] = {
            k: list(v) for k, v in groupby(sorted_objects, key=attrgetter("root_folder"))
        }
        for root_folder, objects in objects_by_root_folder.items():
            await self._save_dict(
                f"{self.root_key}:{root_folder}",
                {o.id: json.dumps({"path": str(o.path), "name": o.name}) for o in objects},
            )

    async def save_root_folders(self, folders: List[str]):
        await self._delete_key(self.root_key_folders)
        await self._add_to_list(self.root_key_folders, *folders)

    async def get_root_folders(self) -> List[str]:
        return await self._get_list(self.root_key_folders)

    async def get(self, object_id: str, root_folder: str) -> Tuple[Path, str] | None:
        data = await self._get_value_from_dict(f"{self.root_key}:{root_folder}", object_id)
        if not data:
            return None
        data = json.loads(data)
        return Path(data["path"]), data["name"]

    async def get_multi(self, object_ids: List[str], root_folder: str) -> List[Tuple[Path, str]]:
        data = await self._get_values_from_dict(f"{self.root_key}:{root_folder}", object_ids)
        data = [json.loads(item) for item in data]
        return [(Path(item["path"]), item["name"]) for item in data]

    async def clear_path_cache(self):
        folders = await self._get_list(self.root_key_folders)
        await asyncio.gather(*[self._delete_key(f"{self.root_key}:{root_folder}") for root_folder in folders])
