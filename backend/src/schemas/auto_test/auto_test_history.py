from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Set

from pydantic import BaseModel

from src.utils.pydantic_helper import all_optional

from .auto_test import Asset
from .common import ResultByStatus, TestError


class StatusEnum(StrEnum):
    pending = "pending"
    success = "success"
    fail = "fail"


class StageEnum(StrEnum):
    group_setup = "group_setup"
    setup = "setup"
    call = "call"
    teardown = "teardown"
    group_teardown = "group_teardown"


class StageResult(BaseModel):
    status: StatusEnum = StatusEnum.pending
    steps_data: list = []
    errors: List[TestError] = []


class AutoTestStages(BaseModel):
    group_setup: StageResult = StageResult()
    setup: StageResult = StageResult()
    call: StageResult = StageResult()
    teardown: StageResult = StageResult()
    group_teardown: StageResult = StageResult()


class Step(BaseModel):
    name: str
    status: StatusEnum = StatusEnum.pending
    inner: List[Step] | None = None


class AutoTestHistoryDB(BaseModel):
    test_id: str
    test_run_id: str
    run_config: Dict
    groups: List[str]

    status: StatusEnum = StatusEnum.pending
    stages: AutoTestStages | None = None
    env_used: Dict[str, str] = {}
    warnings: List[str] = []
    assets_path: Dict[str, Asset] = {}
    generated_params: Dict[str, str] = {}
    errors: Dict[StageEnum, List[TestError]] = {}


class AutoTestHistory(AutoTestHistoryDB):
    iteration_name: str
    method_name: str
    params: Dict
    description: str | None = None


@all_optional
class AutoTestHistoryUpdate(AutoTestHistory):
    pass


class ResultTreeStatus(StrEnum):
    idle = "idle"
    pending = "pending"
    finished = "finished"
    failed = "failed"


class AutoTestGroup(BaseModel):
    id: str
    name: str
    root: bool = False
    groups: Set[str] = set()
    auto_tests: Set[str] = set()
    result_by_status: ResultByStatus | None = ResultByStatus()


class AutoTestItem(BaseModel):
    name: str
    status: StatusEnum


class TestResultTree(BaseModel):
    status: ResultTreeStatus
    first_level: List[str] | None = None
    groups: Dict[str, AutoTestGroup] | None = None
    items: Dict[str, AutoTestItem] | None = None


class AutoTestStatistic(BaseModel):
    date: datetime
    status: StatusEnum


class AutoTestStatisticResponse(BaseModel):
    full_name: str
    result_by_status: ResultByStatus
    statistic: List[AutoTestStatistic]
