import uuid
from typing import List

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from src import crud, models
from src.api import deps
from src.cache.load_test.public_event_channel import LoadTestEventManager
from src.modules.load_test_runner.collector import Collector
from src.modules.load_test_runner.manager import LoadTestManager
from src.modules.load_test_runner.reporter import LoadTestReporter
from src.schemas.load_test.load_test import (
    ChangeNumberOfWorkersRequest,
    CollectedLoadTest,
    LoadTestDB,
    StartLoadTestRequest,
    StartLoadTestResponse,
    StopLoadTestRequest,
)
from src.schemas.load_test.load_test_history import LoadTestHistoryFull

router = APIRouter()


@router.post("/collect/")
async def collect(db: AsyncSession = Depends(deps.get_db)):
    collector = Collector()
    await collector.collect_and_save_load_tests_in_db(db)
    return {"success": True}


@router.post("/dev/recollect/")
async def load_test_recollect(
    db: AsyncSession = Depends(deps.get_db),
):
    collector = Collector()
    await collector.path_cache.clear_path_cache()
    await collector.clear_collected_load_tests_cache()
    await crud.script_history.clear_history(db)
    await crud.load_test.clear(db)
    await collector.collect_and_save_load_tests_in_db(db)
    await collector.prime_collected_cache(db)
    return {"success": True}


@router.get("/")
async def get(
    root_folder: str, db: AsyncSession = Depends(deps.get_db), redis: Redis = Depends(deps.get_redis)
) -> List[CollectedLoadTest]:
    return await Collector().get_collected_load_tests(db, root_folder)


@router.get("/root_folders/")
async def get():
    return await Collector().get_collected_folders()


@router.get("/{load_test_id}/")
async def get_load_test(
    load_test_id: str,
    db: AsyncSession = Depends(deps.get_db),
) -> LoadTestDB:
    return await Collector().get_load_test_by_id(db, load_test_id)


@router.post("/start/")
async def start(request: StartLoadTestRequest, user: models.User = Depends(deps.get_user)) -> StartLoadTestResponse:
    execution_id = str(uuid.uuid4())
    await LoadTestReporter(load_test_id=request.load_test_id).start_report(execution_id, user, request)
    await LoadTestManager(load_test_id=request.load_test_id).start(execution_id)
    return StartLoadTestResponse(execution_id=execution_id)


@router.post("/stop/")
async def stop(request: StopLoadTestRequest):
    await LoadTestManager(load_test_id=request.load_test_id).stop()


@router.post("/change_number_of_workers/")
async def change_number_of_workers(request: ChangeNumberOfWorkersRequest):
    await LoadTestManager(load_test_id=request.load_test_id).change_number_of_workers(
        request.execution_id, request.config_values, request.number_of_tasks
    )


@router.get("/{load_test_id}/last/")
async def get_last_load_test_history(load_test_id: str) -> LoadTestHistoryFull | None:
    return await LoadTestReporter(load_test_id=load_test_id).get_last_history()


@router.websocket("/ws/history/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await LoadTestEventManager().listen_with_subscription(websocket)
