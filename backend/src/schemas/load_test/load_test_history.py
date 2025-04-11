from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List

from pydantic import BaseModel

from src.schemas.environment import EnvEnum, EnvOverwriteParam
from src.schemas.load_test.load_test import LoadTestConfig
from src.utils.pydantic_helper import all_optional


class LoadTestStatusEnum(StrEnum):
    pending = "pending"
    running = "running"
    finished = "finished"


class LoadTestHistory(BaseModel):
    execution_id: str
    load_test_id: str
    params: Dict[str, str | int | float | bool | List[str | int | float] | None] = {}
    config_values: LoadTestConfig
    chart_config: Dict[str, str] | None = None
    number_of_tasks: int
    status: LoadTestStatusEnum = LoadTestStatusEnum.pending
    root_folder: str
    env_name: EnvEnum
    setting_overwrite: Dict[str, EnvOverwriteParam] = {}
    env_used: Dict[str, str] = {}
    user_id: int

    start_time: datetime
    end_time: datetime | None = None


@all_optional
class LoadTestHistoryUpdate(LoadTestHistory):
    pass


class LoadTestWorkerStatusEnum(StrEnum):
    pending = "pending"
    working = "working"
    finished = "finished"


class LoadTestTaskStatusEnum(StrEnum):
    pending = "pending"
    setup = "setup"
    working = "working"
    teardown = "teardown"
    finished = "finished"


class LoadTestTaskStatusHistory(BaseModel):
    pending: int = 0
    setup: int = 0
    working: int = 0
    teardown: int = 0
    finished: int = 0


class WorkerFinishedException(BaseException):
    pass


class SupervisorFinishedException(BaseException):
    pass


class LoadTestHistoryFull(LoadTestHistory):
    workers: Dict[str, LoadTestWorkerStatusEnum]
    task_status_history: Dict[str, LoadTestTaskStatusHistory]
    charts: Dict[str, Any]
