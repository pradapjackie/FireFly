import asyncio
import itertools
from collections import defaultdict
from itertools import groupby
from operator import attrgetter
from typing import Dict, List

from src.cache.base import CacheBase
from src.core.config import settings
from src.schemas.auto_test.auto_test import AutoTest


class AutoTestTagsCache(CacheBase[Dict, Dict]):
    def __init__(self):
        self.root_key = f"collected_autotest_tags_{settings.PROJECT_VERSION}"
        super().__init__()

    @staticmethod
    def _classes_to_tag_dict(tests: List[AutoTest]) -> Dict[str, List[AutoTest]]:
        tag_dict = defaultdict(list)
        for test in tests:
            if test.test_class.tags:
                for tag in test.test_class.tags:
                    tag_dict[tag].append(test)
        return tag_dict

    async def _save_tag(self, root_folder: str, tag: str, test_ids: List[str]):
        await self._add_to_set(f"{self.root_key}:{root_folder}", tag)
        await self._add_to_set(f"{self.root_key}:{root_folder}:{tag}", *test_ids)

    async def save_tags(self, tests: List[AutoTest], collected_root_folders: List[str]):
        await self.clear_all_tags(collected_root_folders)
        sorted_tests = sorted(tests, key=lambda x: x.root_folder)
        tests_by_folder = {k: list(v) for k, v in groupby(sorted_tests, key=attrgetter("root_folder"))}
        for root_folder, tests in tests_by_folder.items():
            tests_by_tag = self._classes_to_tag_dict(tests)
            for tag, tests in tests_by_tag.items():
                await self._save_tag(root_folder, tag, [test.id for test in tests])

    async def get_by_tags(self, tags: List[str], root_folder: str) -> List[str]:
        data = await asyncio.gather(*[self._get_set(f"{self.root_key}:{root_folder}:{tag}") for tag in tags])
        return list(itertools.chain.from_iterable(data))

    async def delete_by_folder(self, root_folder: str):
        tags = await self._get_set(f"{self.root_key}:{root_folder}")
        tags and await asyncio.gather(*[self._delete_key(f"{self.root_key}:{root_folder}:{tag}") for tag in tags])
        await self._delete_key(f"{self.root_key}:{root_folder}")

    async def clear_all_tags(self, collected_root_folders: List[str]):
        await asyncio.gather(*[self.delete_by_folder(root_folder) for root_folder in collected_root_folders])
