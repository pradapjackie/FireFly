from datetime import datetime
from sys import exc_info
from traceback import format_exc, format_exception
from typing import Any, Dict, List, Tuple

import pendulum
from pendulum import now
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.cache.script_runner.script_event_channel import ScriptEventChannel
from src.cache.script_runner.script_history import ScriptHistoryCache
from src.cache.script_runner.script_history_log import ScriptHistoryLogCache
from src.cache.script_runner.script_last import ScriptLastCache
from src.db.session import SessionLocal
from src.models import User
from src.modules.script_runner.contexts import ScriptExecutionContext
from src.modules.script_runner.script_file_result import FileResult
from src.schemas.script_runner.script import StartScriptRequest
from src.schemas.script_runner.script_history import (
    ScriptError,
    ScriptFullHistory,
    ScriptHistory,
    ScriptHistoryDB,
    ScriptHistoryDisplay,
    ScriptHistoryUpdate,
    ScriptMultiResult,
    ScriptResult,
    ScriptResultTypeEnum,
    ScriptStatusEnum,
)
from src.utils.compare_pydantic_models import AnyEqualMixin
from src.utils.list_utils import all_items_in_list_equal


class Reporter:
    def __init__(self, script_id: str, db_session_maker: AsyncSession | None = None):
        self.script_id = script_id
        self.db_session = db_session_maker if db_session_maker else SessionLocal
        self.history_cache = ScriptHistoryCache(script_id)
        self.last_script_cache = ScriptLastCache()
        self.history_log_cache = ScriptHistoryLogCache(script_id)
        self.event_channel = ScriptEventChannel()
        self.supported_result_string_types = (
            str,
            int,
            float,
            bool,
            bytes,
            datetime,
            pendulum.DateTime,
            pendulum.Date,
            AnyEqualMixin,
            type(None),
        )

    async def start_script_report(self, execution_id: str, user: User, start_request: StartScriptRequest):
        new_script_history = ScriptHistory(
            execution_id=execution_id,
            script_id=self.script_id,
            params=start_request.params,
            user_id=user.id,
            root_folder=start_request.root_folder,
            env_name=start_request.env_name,
            setting_overwrite=start_request.setting_overwrite,
            start_time=now(tz="UTC"),
        )
        await self.history_cache.create(execution_id, new_script_history)
        await self.last_script_cache.save(self.script_id, execution_id)

    async def add_log(self, execution_id: str, message: str):
        line_number = await self.history_log_cache.add(execution_id, message)
        await self.event_channel.add_log(
            script_id=self.script_id, execution_id=execution_id, index=line_number, line=message
        )

    def _is_flat_dict(self, d: Dict) -> bool:
        return isinstance(d, dict) and all(
            isinstance(value, self.supported_result_string_types) for value in d.values()
        )

    def _is_flat_model(self, model: BaseModel) -> bool:
        return isinstance(model, BaseModel) and all(
            isinstance(value, self.supported_result_string_types) for value in model.model_dump().values()
        )

    def _is_list_of_flat_dicts(self, list_result: List[Dict]) -> bool:
        return all(self._is_flat_dict(item) for item in list_result) and all_items_in_list_equal(
            [item.keys() for item in list_result]
        )

    def _is_list_of_flat_models(self, list_result: List[BaseModel]) -> bool:
        return all(self._is_flat_model(item) for item in list_result) and all_items_in_list_equal(
            [item.model_dump().keys() for item in list_result]
        )

    async def _format_result(self, result: Any) -> Tuple[ScriptResult, List[Exception] | None]:
        errors = None
        if isinstance(result, List):
            if not isinstance(result, ScriptMultiResult):
                errors = [item for item in result if isinstance(item, Exception)]
                result = [item for item in result if not isinstance(item, Exception)]

        match result:
            case ScriptMultiResult():
                inner_results, inner_errors = {}, []
                for i, r in enumerate(result):
                    r, e = await self._format_result(r)
                    inner_results[i] = r
                    e and inner_errors.extend(e)
                return ScriptResult(type=ScriptResultTypeEnum.multi, object=inner_results), inner_errors
            case FileResult():
                return await result.get_script_result(), errors
            case dict() if self._is_flat_dict(result):
                return ScriptResult(type=ScriptResultTypeEnum.object, object=result), errors
            case BaseModel() if self._is_flat_model(result):
                return ScriptResult(type=ScriptResultTypeEnum.object, object=result.model_dump()), errors
            case list() if all(isinstance(obj, FileResult) for obj in result):
                return (
                    ScriptResult(
                        type=ScriptResultTypeEnum.files, object=[await item.get_script_result() for item in result]
                    ),
                    errors,
                )
            case list() if self._is_list_of_flat_dicts(result):
                return ScriptResult(type=ScriptResultTypeEnum.table, object=result), errors
            case list() if self._is_list_of_flat_models(result):
                return (
                    ScriptResult(type=ScriptResultTypeEnum.table, object=[item.model_dump() for item in result]),
                    errors,
                )
            case _:
                try:
                    return ScriptResult(type=ScriptResultTypeEnum.string, object=str(result)), errors
                except Exception as e:
                    raise NotImplementedError(
                        f"Script {self.script_id} returns unsupported result type. "
                        f"During converting it to string, the following error occurs: {e}"
                    ) from e

    async def _save_script_report_in_db(self, execution_id: str):
        script_report = await self.history_cache.get(execution_id)
        script_report_in_db = ScriptHistoryDB(
            id=script_report.execution_id,
            script_id=script_report.script_id,
            params=script_report.params,
            status=script_report.status,
            root_folder=script_report.root_folder,
            environment=script_report.env_name,
            env_used=script_report.env_used,
            result_type=script_report.result.type if script_report.result else None,
            result=script_report.result.object if script_report.result else None,
            errors=script_report.errors,
            user_id=script_report.user_id,
            start_time=script_report.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time=script_report.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        )
        try:
            async with self.db_session() as db:
                await crud.script_history.create(db, obj_in=script_report_in_db)
        except Exception as e:
            print(f"Exception during saving script report in db: {e}")
            raise e

    async def update_script_report_with_async_gen_result(self, execution_id: str, result: Any, result_number: int):
        result, errors = await self._format_result(result)
        if errors:
            errors = [
                ScriptError(name=type(exc).__name__, message=str(exc), traceback="".join(format_exception(exc)))
                for exc in errors
            ]
        current_history = await self.history_cache.get(execution_id)
        new_result = current_history.result or ScriptResult(type=ScriptResultTypeEnum.multi, object={})
        new_result.object[result_number] = result
        new_errors = (current_history.errors or []) + (errors or [])
        await self.history_cache.update(execution_id, ScriptHistoryUpdate(result=new_result, errors=new_errors))
        await self.event_channel.add_intermediate_result(self.script_id, execution_id, {result_number: result})
        errors and await self.event_channel.add_intermediate_errors(self.script_id, execution_id, errors)

    async def finish_script_report(self, execution_id: str, result: Any, context: ScriptExecutionContext):
        result, errors = await self._format_result(result)
        status = ScriptStatusEnum.success
        if errors:
            status = ScriptStatusEnum.partial_success if result else ScriptStatusEnum.fail
            errors = [
                ScriptError(name=type(exc).__name__, message=str(exc), traceback="".join(format_exception(exc)))
                for exc in errors
            ]

        update = ScriptHistoryUpdate(
            status=status, result=result, env_used=context.env_used, errors=errors, end_time=now(tz="UTC")
        )
        await self.history_cache.update(execution_id, update)
        await self.event_channel.add_result(self.script_id, execution_id, result)
        errors and await self.event_channel.add_errors(self.script_id, execution_id, errors)
        await self.event_channel.add_env_used(self.script_id, execution_id, context.env_used)
        await self.event_channel.update_status(self.script_id, execution_id, status)
        await self.event_channel.close_channel(execution_id)
        await self._save_script_report_in_db(execution_id)

    async def finish_script_report_with_error(
        self, execution_id: str, error: Exception, context: ScriptExecutionContext, phase_name: str = ""
    ):
        error_prefix = f"Exception during '{phase_name}' script execution phase: " if phase_name else ""
        if isinstance(error, ExceptionGroup):
            errors = [
                ScriptError(
                    name=error_prefix + type(exc).__name__, message=str(exc), traceback="".join(format_exception(exc))
                )
                for exc in error.exceptions
            ]
        else:
            exc_type, value, _ = exc_info()
            errors = [ScriptError(name=error_prefix + exc_type.__name__, message=str(error), traceback=format_exc())]
        update = ScriptHistoryUpdate(
            status=ScriptStatusEnum.fail, errors=errors, env_used=context.env_used, end_time=now(tz="UTC")
        )
        await self.history_cache.update(execution_id, update)
        await self.event_channel.add_errors(self.script_id, execution_id, errors)
        await self.event_channel.add_env_used(self.script_id, execution_id, context.env_used)
        await self.event_channel.update_status(self.script_id, execution_id, ScriptStatusEnum.fail)
        await self.event_channel.close_channel(execution_id)
        await self._save_script_report_in_db(execution_id)

    async def get_script_history(self, execution_id: str) -> ScriptFullHistory:
        script_history = await self.history_cache.get(execution_id)
        log = await self.history_log_cache.get(execution_id)
        return ScriptFullHistory(**script_history.model_dump(), log=log)

    async def get_last_script_history(self) -> ScriptFullHistory | None:
        if last_execution_id := await self.last_script_cache.get(self.script_id):
            return await self.get_script_history(last_execution_id)

    async def get_script_history_records(self) -> ScriptHistoryDisplay:
        async with self.db_session() as db:
            result = await crud.script.get_script_history(db, script_id=self.script_id)
            for item in result.history:
                item.log = await self.history_log_cache.get(item.execution_id)
            return result
