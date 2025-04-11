import asyncio
import uuid
from typing import List

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models
from src.api import deps
from src.cache.script_runner.script_event_channel import ScriptEventManager
from src.modules.script_runner.collector import Collector
from src.modules.script_runner.manager import ScriptManager
from src.modules.script_runner.reporter import Reporter
from src.schemas.script_runner.script import CollectedScript, ScriptDB, StartScriptRequest, StartScriptResponse
from src.schemas.script_runner.script_history import ScriptFullHistory, ScriptHistoryDisplay

router = APIRouter()


@router.post("/collect/")
async def collect(db: AsyncSession = Depends(deps.get_db)):
    collector = Collector()
    await collector.collect_and_save_scripts_in_db(db)
    return {"success": True}


@router.post("/dev/recollect/")
async def recollect(db: AsyncSession = Depends(deps.get_db)):
    collector = Collector()
    await collector.path_cache.clear_path_cache()
    await collector.clear_collected_scripts_cache()
    await crud.script_history.clear_history(db)
    await crud.script.clear(db)
    await collector.collect_and_save_scripts_in_db(db)
    await collector.prime_collected_cache(db)
    return {"success": True}


@router.get("/")
async def get(
    root_folder: str,
    db: AsyncSession = Depends(deps.get_db),
) -> List[CollectedScript]:
    return await Collector().get_collected_scripts(db, root_folder)


@router.get("/root_folders/")
async def get():
    return await Collector().get_collected_folders()


@router.get("/{script_id}/")
async def get_script(
    script_id: str,
    db: AsyncSession = Depends(deps.get_db),
) -> ScriptDB:
    return await Collector().get_script_by_id(db, script_id)


@router.get("/{script_id}/last/")
async def get_last_script_history(script_id: str) -> ScriptFullHistory | None:
    return await Reporter(script_id=script_id).get_last_script_history()


@router.get("/{script_id}/history/")
async def get_script_history_records(script_id: str) -> ScriptHistoryDisplay:
    return await Reporter(script_id=script_id).get_script_history_records()


@router.get("/{script_id}/{execution_id}/")
async def get_one_script_history(script_id: str, execution_id: str) -> ScriptFullHistory:
    return await Reporter(script_id=script_id).get_script_history(execution_id)


@router.post("/run/")
async def run(request: StartScriptRequest, user: models.User = Depends(deps.get_user)) -> StartScriptResponse:
    execution_id = str(uuid.uuid4())
    await Reporter(script_id=request.script_id).start_script_report(execution_id, user, request)
    # noinspection PyAsyncCall
    asyncio.create_task(ScriptManager(script_id=request.script_id).run_script(execution_id=execution_id))
    return StartScriptResponse(execution_id=execution_id)


@router.websocket("/ws/history/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await ScriptEventManager().listen_with_subscription(websocket)
