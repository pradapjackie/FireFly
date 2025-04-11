from typing import Dict, Type

from pydantic import BaseModel, ConfigDict

from src.core.config import settings
from src.modules.load_test_runner.load_test_abs import LoadTestAbc
from src.schemas.common import CollectedObject
from src.schemas.environment import EnvEnum, EnvOverwriteParam
from src.utils.dynamic_form import Field
from src.utils.hash_funcs import md5
from src.utils.pydantic_helper import UpdatableModel


class RegisteredLoadTest(CollectedObject):
    callable: Type[LoadTestAbc]


class LoadTestConfig(UpdatableModel):
    maximum_number_of_workers: int
    concurrency_within_a_single_worker: int

    model_config = ConfigDict(extra="allow")


class LoadTest(RegisteredLoadTest):
    params: Dict[str, Field]
    charts: Dict[str, str]
    config: LoadTestConfig

    @property
    def id(self) -> str:
        prefix = "".join(c for c in self.name if c.isalpha() or c == "_")
        params_hash = md5("".join([str(self.path), str(self.params)]))
        return prefix + params_hash


class LoadTestDB(BaseModel):
    id: str
    name: str
    display_name: str
    description: str | None = None
    root_folder: str
    filepath: str
    params: Dict
    charts: Dict
    config: LoadTestConfig
    supported_from: str = settings.PROJECT_VERSION
    supported_to: str = settings.PROJECT_VERSION

    model_config = ConfigDict(from_attributes=True)


class CollectedLoadTest(BaseModel):
    id: str
    display_name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class StartLoadTestRequest(BaseModel):
    root_folder: str
    env_name: EnvEnum
    setting_overwrite: Dict[str, EnvOverwriteParam]
    load_test_id: str
    params: Dict
    config_values: LoadTestConfig
    number_of_tasks: int
    chart_config: Dict[str, str] | None = None


class StartLoadTestResponse(BaseModel):
    execution_id: str


class StopLoadTestRequest(BaseModel):
    load_test_id: str


class ChangeNumberOfWorkersRequest(BaseModel):
    load_test_id: str
    execution_id: str
    config_values: LoadTestConfig
    number_of_tasks: int
