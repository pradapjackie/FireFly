from datetime import datetime
from enum import StrEnum
from typing import Dict, List

from pydantic import BaseModel

from src.utils.pydantic_helper import all_optional

from ..environment import EnvEnum, EnvOverwriteParam
from ..user import User
from .common import ResultByStatus, TestError


class TestRunStatus(StrEnum):
    idle = "idle"
    pending = "pending"
    primed = "primed"
    running = "running"
    success = "success"
    fail = "fail"


class StartTestRunRequest(BaseModel):
    root_folder: str
    env_name: EnvEnum
    test_ids: List[str]
    tags: List[str] = []
    setting_overwrite: Dict[str, EnvOverwriteParam]
    run_config: Dict


class TestRun(StartTestRunRequest):
    id: str
    user: User
    version: str
    status: TestRunStatus = TestRunStatus.idle
    result_by_status: ResultByStatus | None = ResultByStatus()
    error: TestError | None = None
    group_ids: List[str] = []

    start_time: datetime


class TestRunDB(BaseModel):
    id: str
    user_id: int
    version: str
    status: TestRunStatus
    result_by_status: ResultByStatus
    start_time: datetime
    root_folder: str
    environment: str
    run_config: Dict
    error: TestError | None = None
    group_ids: List[str]


@all_optional
class TestRunUpdate(TestRun):
    pass


class StartTestRunResponse(BaseModel):
    id: str
    status: TestRunStatus
    result_by_status: ResultByStatus = ResultByStatus()
    start_time: datetime


class TestRunListResponse(BaseModel):
    ids: List[str]
    runs: Dict[str, TestRun]


class TestRunStatisticResponse(BaseModel):
    stat: ResultByStatus
    test_runs: List[TestRun]
