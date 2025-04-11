import asyncio
import re
from functools import lru_cache
from inspect import getdoc, getmembers, isfunction
from typing import Dict, Generator, List, MutableMapping, Tuple, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.cache import AutoTestPathsCache, AutoTestTagsCache
from src.cache.auto_test.auto_test_cache import AutoTestCache
from src.modules.auto_test.config import settings
from src.modules.auto_test.register import register
from src.modules.auto_test.test_abs import TestAbs
from src.modules.auto_test.utils import helpers
from src.modules.base_collector import BaseCollector
from src.schemas.auto_test.auto_test import (
    AutoTest,
    AutoTestDB,
    CollectedTestsResponse,
    RegisteredTest,
    TestClass,
    TestMethod,
)
from src.schemas.common import CollectObjectTypes
from src.utils import format
from src.utils.dynamic_form import Field
from src.utils.rate_limiter import RedisLock


class Collector(BaseCollector):
    def __init__(self):
        self.class_name_replace_pattern = re.compile("(?<![A-Z])(?<!^)([A-Z])")
        self.method_name_replace_pattern = re.compile("(test_|_test)")
        self.paths_cache = AutoTestPathsCache()
        self.auto_test_tags_cache = AutoTestTagsCache()
        self.collected_cache = AutoTestCache()

    @staticmethod
    def create_iteration(params: Dict) -> Tuple[str, Dict]:
        iteration_names = {key: params[key] for key in params.keys() & settings.ITERATION_NAMES}
        if len(iteration_names) > 1:
            raise RuntimeError(f"More than one name specified for iteration: {params}")
        else:
            iteration_name = next(iter(iteration_names.values()))
        params = {key: params[key] for key in params.keys() if key not in settings.ITERATION_NAMES}
        return iteration_name, params

    @staticmethod
    @lru_cache
    def get_cls_methods(test_class: Type[TestAbs]) -> List[TestMethod]:
        all_methods = [
            TestMethod(name=bare_method[0], description=getdoc(bare_method[1]), func=bare_method[1])
            for bare_method in getmembers(test_class, predicate=isfunction)
        ]
        return [method for method in all_methods if re.search(settings.TEST_METHOD_PATTERN, method.name)]

    @staticmethod
    @lru_cache
    def get_cls_run_config(test_class: TestClass) -> Dict[str, Field]:
        result = {}
        if config_cls := getattr(test_class.cls, "RunConfig", None):
            for alias, field in getmembers(config_cls, predicate=lambda x: isinstance(x, Field)):
                result[alias] = field
        return result

    def get_method_iterations(self, method: TestMethod) -> Generator[Tuple[str, Dict], None, None]:
        iterations = getattr(method.func, "iterations", [{}])
        return (self.create_iteration(data) for data in iterations)

    @staticmethod
    def get_run_in_separate_thread(method: TestMethod):
        return getattr(method.func, "run_in_separate_thread", False)

    def convert_registered_tests_to_autotests(self, collected_tests: List[RegisteredTest]) -> List[AutoTest]:
        result: List[AutoTest] = []
        for registered_test in collected_tests:
            test_class = TestClass(
                cls=registered_test.callable,
                name=registered_test.callable.__name__,
                filepath=registered_test.path,
                tags=registered_test.callable.tags,
            )
            for test_method in self.get_cls_methods(registered_test.callable):
                for iteration_name, params in self.get_method_iterations(test_method):
                    result.append(
                        AutoTest(
                            test_class=test_class,
                            test_method=test_method,
                            iteration_name=iteration_name,
                            params=params,
                            root_folder=registered_test.root_folder,
                            filepath=".".join(registered_test.path.relative_to(settings.ROOT_PATH).parts[1:-1]),
                            run_config={},
                            run_in_separate_thread=self.get_run_in_separate_thread(test_method),
                        )
                    )
        return result

    async def collect_tests(self, root_folder: str | None = None) -> List[AutoTest]:
        async with RedisLock(name="Test collection", timeout=60 * 10):
            collected_root_folders = self.collect_root_folders(root_path=settings.ROOT_PATH)
            collected_tests: List[RegisteredTest] = await self.collect(
                root_path=settings.ROOT_PATH,
                acceptable_types_of_objects=[CollectObjectTypes.class_],
                collected_type=RegisteredTest,
                decorator=register,
                root_folder=root_folder,
            )
            result = self.convert_registered_tests_to_autotests(collected_tests)
            await self.paths_cache.save_root_folders(collected_root_folders)
            await self.paths_cache.save_paths(result)
            await self.auto_test_tags_cache.save_tags(result, collected_root_folders)
        return result

    async def get_collected_folders(self) -> List[str]:
        return await self.paths_cache.get_root_folders()

    async def collect_test_by_ids(self, test_ids: List[str], root_folder: str) -> List[AutoTest]:
        collected_paths = await self.paths_cache.get_multi(test_ids, root_folder)
        collected_tests: List[RegisteredTest] = []
        for test_path, test_class_name in set(collected_paths):
            collected_tests.append(
                self.import_from_file(
                    root_path=settings.ROOT_PATH,
                    file_path=test_path,
                    object_name=test_class_name,
                    collected_type=RegisteredTest,
                )
            )
        auto_tests = self.convert_registered_tests_to_autotests(collected_tests)
        return list(set(auto_test for auto_test in auto_tests if auto_test.id in test_ids))

    async def collect_and_save_tests_in_db(self, db: AsyncSession, root_folder: str | None = None) -> None:
        collected_tests = await self.collect_tests(root_folder=root_folder)
        auto_test_to_create = []
        for test in collected_tests:
            auto_test_to_create.append(
                AutoTestDB(
                    id=test.id,
                    method_name=format.format_method_name(test.test_method.name),
                    class_name=format.format_class_name(test.test_class.name),
                    iteration_name=test.iteration_name,
                    root_folder=test.root_folder,
                    filepath=test.filepath,
                    params=test.params,
                    description=test.test_method.description,
                    required_run_config=self.get_cls_run_config(test.test_class),
                )
            )
        await crud.auto_test.add_auto_tests(db, auto_test_to_create)

    async def get_collected_tests(self, db: AsyncSession, root_folder: str) -> CollectedTestsResponse:
        if result := await self.collected_cache.get(root_folder):
            return result

        auto_tests = await crud.auto_test.get_auto_tests(db, root_folder)
        group_result = helpers.generate_group_response(auto_tests)
        auto_test_result = helpers.generate_collected_test_result(auto_tests)
        result = CollectedTestsResponse(groups=group_result, items=auto_test_result)

        if auto_tests:
            await self.collected_cache.save(root_folder, result)

        return result

    async def prime_collected_cache(self, db: AsyncSession):
        for root_folder in await self.paths_cache.get_root_folders():
            await self.get_collected_tests(db, root_folder)

    async def clear_collected_tests_cache(self):
        folders = await self.paths_cache.get_root_folders()
        await asyncio.gather(*[self.collected_cache.delete(root_folder) for root_folder in folders])

    @staticmethod
    def prime_tests_with_env(env, auto_tests: List[AutoTest]):
        prefix = env.prefix
        for auto_test in auto_tests:
            for param_name, param_value in auto_test.params.items():
                if isinstance(param_value, str) and param_value.startswith(prefix):
                    auto_test.params[param_name] = getattr(env, param_value[len(prefix) :])

    def prime_tests_with_run_config(self, run_config: MutableMapping, auto_tests: List[AutoTest]):
        for auto_test in auto_tests:
            for name, field in self.get_cls_run_config(auto_test.test_class).items():
                field.value = run_config.get(name, field.default_value)
                auto_test.run_config[name] = run_config.get(name, field.default_value)
