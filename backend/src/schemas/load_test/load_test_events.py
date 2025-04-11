from enum import StrEnum
from typing import Any, Dict

from pydantic import BaseModel

from src.schemas.load_test.load_test_history import LoadTestTaskStatusHistory, LoadTestWorkerStatusEnum


class LoadTestEventTypeEnum(StrEnum):
    execution = "execution"
    worker = "worker"
    task = "task"
    chart = "chart"


class LoadTestEvent(BaseModel):
    type: LoadTestEventTypeEnum
    data: Any


class ExecutionMessage(BaseModel):
    load_test_id: str
    update: Dict


class WorkerMessage(BaseModel):
    load_test_id: str
    worker_id: str
    status: LoadTestWorkerStatusEnum


class TaskHistoryMessage(BaseModel):
    load_test_id: str
    now_string: str
    data: LoadTestTaskStatusHistory


class ChartMessage(BaseModel):
    load_test_id: str
    chart_name: str
    data: Any


class LoadTestExecutionEvent(LoadTestEvent):
    type: LoadTestEventTypeEnum = LoadTestEventTypeEnum.execution
    data: ExecutionMessage


class LoadTestWorkerEvent(LoadTestEvent):
    type: LoadTestEventTypeEnum = LoadTestEventTypeEnum.worker
    data: WorkerMessage


class LoadTestTaskHistoryEvent(LoadTestEvent):
    type: LoadTestEventTypeEnum = LoadTestEventTypeEnum.task
    data: TaskHistoryMessage


class LoadTestChartEvent(LoadTestEvent):
    type: LoadTestEventTypeEnum = LoadTestEventTypeEnum.chart
    data: ChartMessage


# Internal command channel


class LoadTestInternalEventTypeEnum(StrEnum):
    stop_all_workers = "stop_all_workers"
    stop_specific_worker = "stop_specific_worker"
    worker_status_update = "worker_status_update"
    start_task_updates = "start_task_updates"


class LoadTestInternalEvent(BaseModel):
    type: LoadTestInternalEventTypeEnum
    data: Any = None


class LoadTestStopWorkersEvent(LoadTestInternalEvent):
    type: LoadTestInternalEventTypeEnum = LoadTestInternalEventTypeEnum.stop_all_workers


class LoadTestStopSpecificWorkerEvent(LoadTestInternalEvent):
    type: LoadTestInternalEventTypeEnum = LoadTestInternalEventTypeEnum.stop_specific_worker
    data: str


class WorkerStatusInternalUpdate(BaseModel):
    worker_id: str
    status: LoadTestWorkerStatusEnum


class LoadTestWorkerStatusUpdate(LoadTestInternalEvent):
    type: LoadTestInternalEventTypeEnum = LoadTestInternalEventTypeEnum.worker_status_update
    data: WorkerStatusInternalUpdate


class LoadTestStartTaskUpdatesEvent(LoadTestInternalEvent):
    type: LoadTestInternalEventTypeEnum = LoadTestInternalEventTypeEnum.start_task_updates
