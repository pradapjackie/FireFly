import asyncio
import inspect
from typing import Dict, List, Type

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.cache.load_test.load_test_cache import LoadTestCache
from src.cache.load_test.paths import LoadTestPathsCache
from src.modules.base_collector import BaseCollector
from src.modules.load_test_runner.charts.base import BaseChart
from src.modules.load_test_runner.config import settings
from src.modules.load_test_runner.load_test_abs import LoadTestAbc
from src.schemas.common import CollectObjectTypes
from src.schemas.load_test.load_test import CollectedLoadTest, LoadTest, LoadTestConfig, LoadTestDB, RegisteredLoadTest
from src.utils.dynamic_form import Field
from src.utils.format import format_class_or_method_name
from src.utils.rate_limiter import RedisLock


class Collector(BaseCollector):
    def __init__(self):
        self.path_cache = LoadTestPathsCache()
        self.collected_cache = LoadTestCache()

    def get_params(self, load_test: RegisteredLoadTest) -> Dict[str, Field]:
        signature_parameters = list(inspect.signature(load_test.callable.__init__).parameters.values())[1:]
        # Filter ABC Meta __init__ signature
        signature_parameters = [param for param in signature_parameters if param.name not in ("args", "kwargs")]
        return self.signature_to_params(load_test.name, signature_parameters)

    @staticmethod
    def get_charts_config(test_class: Type[LoadTestAbc]) -> Dict[str, str]:
        result = {}
        if config_cls := getattr(test_class, "Charts", None):
            for alias, field in inspect.getmembers(config_cls, predicate=lambda x: isinstance(x, BaseChart)):
                result[alias] = field.__class__.__name__
        return result

    @staticmethod
    def get_execution_config(test_class: Type[LoadTestAbc]) -> LoadTestConfig:
        result = {}
        for test_parent in test_class.__mro__[::-1]:
            if config_cls := getattr(test_parent, "Config", None):
                result.update({k: v for k, v in config_cls.__dict__.items() if not k.startswith("__")})
        return LoadTestConfig(**result)

    async def collect_load_tests(self, root_folder: str | None = None):
        async with RedisLock(name="Load Test collection", timeout=60 * 10):
            collected_root_folders = self.collect_root_folders(root_path=settings.ROOT_PATH)
            collected_tests: List[RegisteredLoadTest] = await self.collect(
                root_path=settings.ROOT_PATH,
                acceptable_types_of_objects=[CollectObjectTypes.class_],
                collected_type=RegisteredLoadTest,
                base_class=LoadTestAbc,
                root_folder=root_folder,
            )
            load_tests = [
                LoadTest(
                    **collected_test.model_dump(),
                    params=self.get_params(collected_test),
                    charts=self.get_charts_config(collected_test.callable),
                    config=self.get_execution_config(collected_test.callable),
                )
                for collected_test in collected_tests
            ]
            await self.path_cache.save_root_folders(collected_root_folders)
            await self.path_cache.save_paths(load_tests)
            return load_tests

    async def get_collected_folders(self) -> List[str]:
        return await self.path_cache.get_root_folders()

    async def collect_and_save_load_tests_in_db(self, db: AsyncSession, root_folder: str | None = None) -> None:
        collected_tests = await self.collect_load_tests(root_folder=root_folder)
        tests_to_save = []
        for test in collected_tests:
            tests_to_save.append(
                LoadTestDB(
                    id=test.id,
                    name=test.name,
                    display_name=format_class_or_method_name(test.name),
                    description=inspect.getdoc(test.callable),
                    root_folder=test.root_folder,
                    filepath=".".join([*test.path.parts[1:-1], test.path.stem]),
                    params=test.params,
                    charts=test.charts,
                    config=test.config,
                )
            )
        await crud.load_test.save_load_tests(db, tests_to_save)

    async def get_collected_load_tests(self, db: AsyncSession, root_folder: str) -> List[CollectedLoadTest]:
        if result := await self.collected_cache.get_list(root_folder):
            return result

        load_tests = await crud.load_test.get_load_tests(db, root_folder)
        result = [CollectedLoadTest.model_validate(load_test) for load_test in load_tests]

        if load_tests:
            await self.collected_cache.save(root_folder, result)

        return result

    async def prime_collected_cache(self, db: AsyncSession):
        for root_folder in await self.path_cache.get_root_folders():
            await self.get_collected_load_tests(db, root_folder)

    async def clear_collected_load_tests_cache(self):
        folders = await self.path_cache.get_root_folders()
        await asyncio.gather(*[self.collected_cache.delete(root_folder) for root_folder in folders])

    @staticmethod
    async def get_load_test_by_id(db: AsyncSession, load_test_id: str) -> LoadTestDB:
        load_test = await crud.load_test.get(db, load_test_id)
        if not load_test:
            raise HTTPException(404, f"No such load test: {load_test_id}")
        return LoadTestDB.model_validate(load_test)

    async def collect_load_test_by_id(self, load_test_id: str, root_folder: str) -> LoadTest:
        script_path, script_name = await self.path_cache.get(load_test_id, root_folder)
        collected_test = self.import_from_file(
            root_path=settings.ROOT_PATH,
            file_path=script_path,
            object_name=script_name,
            collected_type=RegisteredLoadTest,
        )
        return LoadTest(
            **collected_test.model_dump(),
            params=self.get_params(collected_test),
            charts=self.get_charts_config(collected_test.callable),
            config=self.get_execution_config(collected_test.callable),
        )
