import asyncio
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models
from src.api import deps
from src.core.config import settings
from src.modules.auto_test.collector import Collector
from src.modules.auto_test.manager import TestManager
from src.modules.auto_test.reporter import Reporter
from src.modules.environment.env import prime_environment_cache
from src.schemas.auto_test.auto_test_history import AutoTestHistory, TestResultTree
from src.schemas.auto_test.test_run import StartTestRunRequest, StartTestRunResponse, TestRun
from src.schemas.environment import AutoTestEnv, AutoTestEnvUpdate, AutoTestEnvUpdateRequest, EnvEnum
from src.tasks import run_tests

router = APIRouter()


@router.post("/run/")
async def run(params: StartTestRunRequest, user: models.User = Depends(deps.get_user)) -> StartTestRunResponse:
    response = await Reporter(str(uuid.uuid4())).start_test_run_report(user, params)
    if settings.RUN_TEST_IN_MAIN_LOOP:
        asyncio.create_task(TestManager(response.id).run_tests())
    else:
        run_tests.delay(run_id=response.id)
    return response


@router.post("/collect/")
async def collect(db: AsyncSession = Depends(deps.get_db), collector: Collector = Depends(deps.get_autotest_collector)):
    await collector.collect_and_save_tests_in_db(db)
    return {"success": True}


@router.get("/")
async def get(
    root_folder: str,
    db: AsyncSession = Depends(deps.get_db),
    collector: Collector = Depends(deps.get_autotest_collector),
):
    return await collector.get_collected_tests(db, root_folder)


@router.get("/test_runs/")
async def get_test_runs(root_folder: str, env: EnvEnum, db: AsyncSession = Depends(deps.get_db)):
    return await Reporter().get_test_runs(db, root_folder, env)


@router.get("/test_run/statistic/{test_run_id}")
async def get_test_run_statistic(test_run_id: str) -> TestRun:
    reporter = Reporter(test_run_id)
    return await reporter.get_test_run_statistic()


@router.get("/test_run/{test_run_id}/test/{auto_test_id}")
async def get_test_run_item(test_run_id: str, auto_test_id: str) -> AutoTestHistory:
    reporter = Reporter(test_run_id)
    item = await reporter.get_test_run_item(auto_test_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/test_run/tree/{test_run_id}")
async def get_test_run_tree(test_run_id: str) -> TestResultTree:
    reporter = Reporter(test_run_id)
    return await reporter.get_test_run_tree()


@router.get("/stat/")
async def get_statistic(
    root_folder: str,
    env: EnvEnum,
    db: AsyncSession = Depends(deps.get_db),
):
    return await Reporter().get_auto_tests_statistic(db, root_folder, env)


@router.get("/stat/{test_id}")
async def get_auto_test_statistic(test_id: str, db: AsyncSession = Depends(deps.get_db)):
    return await Reporter().get_one_auto_test_statistic(db, test_id)


@router.get("/env")
def get_env_list() -> List:
    return EnvEnum.list()


@router.get("/root_folders/")
async def get(
    collector: Collector = Depends(deps.get_autotest_collector),
):
    return await collector.get_collected_folders()


@router.get("/env/{env_name}")
async def get_env_params(env_name: EnvEnum, db: AsyncSession = Depends(deps.get_db)) -> List[AutoTestEnv]:
    return await crud.auto_test_env.get_env_params(db, env_name)


@router.patch("/env/{env_name}")
async def update_env(
    env_name: EnvEnum,
    data: AutoTestEnvUpdateRequest,
    db: AsyncSession = Depends(deps.get_db),
    redis: Redis = Depends(deps.get_redis),
):
    for item in data.new:
        await crud.auto_test_env.create(db, obj_in=AutoTestEnv(**item.model_dump()))
    for item in data.removed:
        await crud.auto_test_env.remove_env_param(db, env_name=env_name, param=item)
    for item in data.updated:
        await crud.auto_test_env.update_env_param(db, obj_in=AutoTestEnvUpdate(**item.model_dump()))
    await prime_environment_cache(db, redis)


@router.post("/env/prime_cache/")
async def prime_cache(db: AsyncSession = Depends(deps.get_db), redis: Redis = Depends(deps.get_redis)):
    await prime_environment_cache(db, redis)


@router.post("/dev/recollect/")
async def auto_test_recollect(
    db: AsyncSession = Depends(deps.get_db),
    collector: Collector = Depends(deps.get_autotest_collector),
):
    await collector.paths_cache.clear_path_cache()
    await collector.clear_collected_tests_cache()
    await crud.auto_test_history.clear_history(db)
    await crud.auto_test.clear(db)
    await collector.collect_and_save_tests_in_db(db)
    await collector.prime_collected_cache(db)
    return {"success": True}


async def listen_client_disconnect(websocket: WebSocket):
    await websocket.receive_text()


@router.websocket("/ws/test_run/{test_run_id}")
async def websocket_endpoint(websocket: WebSocket, test_run_id: str):
    await websocket.accept()
    reporter = Reporter(test_run_id)

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(listen_client_disconnect(websocket))
            tg.create_task(reporter.test_run_channel.proxy_to_ws(websocket))
    except* WebSocketDisconnect:
        pass
