import json
from itertools import groupby
from operator import attrgetter
from typing import Dict, List

from src.cache.base_path_cache import BasePathsCache
from src.schemas.auto_test.auto_test import AutoTest


class AutoTestPathsCache(BasePathsCache):
    def __init__(self):
        super().__init__(module_name="autotest")

    async def save_paths(self, objects: List[AutoTest]):
        sorted_objects = sorted(objects, key=lambda x: x.root_folder)
        objects_by_root_folder: Dict[str, List[AutoTest]] = {
            k: list(v) for k, v in groupby(sorted_objects, key=attrgetter("root_folder"))
        }
        for root_folder, objects in objects_by_root_folder.items():
            await self._save_dict(
                f"{self.root_key}:{root_folder}",
                {o.id: json.dumps({"path": str(o.test_class.filepath), "name": o.test_class.name}) for o in objects},
            )
