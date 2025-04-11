from enum import StrEnum
from functools import cached_property
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Type

from pydantic import BaseModel

from src.core.config import settings
from src.modules.auto_test.test_abs import TestAbs
from src.schemas.auto_test.common import ResultByStatus
from src.schemas.common import CollectedObject
from src.schemas.environment import EnvUserContext
from src.utils.hash_funcs import md5


class TestClass(BaseModel):
    cls: Type[TestAbs]
    name: str
    filepath: Path
    tags: Optional[List[str]] = None

    def __hash__(self) -> int:
        return hash(self.cls)


class TestMethod(BaseModel):
    name: str
    description: str | None
    func: Callable[[Any, Any], Awaitable[Any]]


class AutoTest(BaseModel):
    test_class: TestClass
    test_method: TestMethod
    iteration_name: str
    params: Dict
    root_folder: str
    filepath: str
    run_config: Dict
    run_in_separate_thread: bool

    @cached_property
    def id(self):
        test_unique_name = (
            f"{self.test_method.name}{self.test_class.name}{self.iteration_name}{self.root_folder}{self.filepath}"
        )
        return "".join([c for c in self.iteration_name if c.isalnum()]).lower() + md5(test_unique_name)

    def __hash__(self) -> int:
        return hash(self.id)


class AutoTestDB(BaseModel):
    id: str
    method_name: str
    class_name: str
    iteration_name: str
    root_folder: str
    filepath: str
    params: Dict
    description: str | None = None
    is_active: bool = True
    supported_from: str = settings.PROJECT_VERSION
    supported_to: str = settings.PROJECT_VERSION
    required_run_config: Dict | None = None


class AssetTypeEnum(StrEnum):
    video = "video"
    text = "text"
    image = "image"


class Asset(BaseModel):
    type: AssetTypeEnum
    title: str
    url: str | None = None


class AutoTestContext(EnvUserContext):
    id: str
    generated_params: Dict[str, str] = {}
    warnings: List[str] = []
    assets_path: Dict[str, Asset] = {}


class CollectedGroup(BaseModel):
    name: str
    status: str | None = None
    groups: Set[str] = set()
    auto_tests: Set[str] = set()
    result_by_status: ResultByStatus | None = None


class CollectedGroupsResponse(BaseModel):
    ids: Set[str] = set()
    first_level: Set[str] = set()
    groups_map: Dict[str, CollectedGroup] = {}


class CollectedTest(BaseModel):
    id: str
    name: str
    required_run_config: Dict


class CollectedAutoTestsResponse(BaseModel):
    ids: Set[str] = set()
    auto_test_map: Dict[str, CollectedTest] = {}


class CollectedTestsResponse(BaseModel):
    groups: CollectedGroupsResponse
    items: CollectedAutoTestsResponse


class RegisteredTest(CollectedObject):
    callable: Type[TestAbs]
