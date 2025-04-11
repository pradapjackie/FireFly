import asyncio
import traceback
from contextlib import asynccontextmanager
from multiprocessing import Pipe, Process
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.cache.script_runner.script_history import ScriptHistoryCache
from src.core.config import settings
from src.modules.environment.env import env
from src.modules.script_runner.collector import Collector
from src.modules.script_runner.contexts import ScriptExecutionContext, script_context
from src.modules.script_runner.reporter import Reporter
from src.modules.script_runner.script_class_abs import ScriptClassAbc
from src.schemas.script_runner.script import Script
from src.schemas.script_runner.script_history import ScriptHistoryUpdate, ScriptMultiResult
from src.utils.async_iterator_utils import a_enumerate


class ScriptManager:
    def __init__(self, script_id: str, db_session_maker: async_sessionmaker[AsyncSession] | None = None):
        self.script_id = script_id
        self.collector = Collector()
        self.reporter = Reporter(script_id, db_session_maker)
        self.script_history_cache = ScriptHistoryCache(script_id)

    @asynccontextmanager
    async def guard(self, phase_name: str, timeout: int = 10 * 60):
        context = script_context.get()
        try:
            async with asyncio.timeout(timeout):
                yield
        except Exception as e:
            await self.reporter.finish_script_report_with_error(context.execution_id, e, context, phase_name)
            raise e

    @staticmethod
    async def _run_script_teardown(script_instance: ScriptClassAbc, params: Dict):
        for script_parent in script_instance.__class__.__mro__:
            if issubclass(script_parent, ScriptClassAbc) and "teardown" in script_parent.__dict__.keys():
                await script_parent.teardown(script_instance, **params)

    async def _run_script_function(self, script: Script, params: Dict, execution_id: str) -> Any:
        if script.is_class_with_async_generator:
            result = ScriptMultiResult()
            script_instance = script.callable()
            try:
                async for i, r in a_enumerate(script_instance.run(**params)):
                    await self.reporter.update_script_report_with_async_gen_result(execution_id, r, i)
                    result.append(r)
            finally:
                await self._run_script_teardown(script_instance, params)
            return result
        elif script.is_async_generator:
            result = ScriptMultiResult()
            async for i, r in a_enumerate(script.callable(**params)):
                await self.reporter.update_script_report_with_async_gen_result(execution_id, r, i)
                result.append(r)
            return result
        elif script.is_class:
            script_instance = script.callable()
            try:
                result = await script_instance.run(**params)
            finally:
                await self._run_script_teardown(script_instance, params)
            return result
        elif script.is_coroutine:
            return await script.callable(**params)
        else:
            raise NotImplementedError(
                f"Script {script.name} type is not supported. "
                f"The script must be an asynchronous function "
                f"or a child of the {ScriptClassAbc.__class__.__name__} class."
            )

    async def run_script_in_sub_process(self, execution_id: str):
        loop = asyncio.get_running_loop()
        parent_conn, child_conn = Pipe()
        p = Process(target=run_memory_intensive_script_in_process, args=(self.script_id, execution_id, child_conn))
        p.start()
        await loop.run_in_executor(None, p.join, None)
        if parent_conn.poll():
            error_data = parent_conn.recv()
            if error_data:
                e, trace = error_data
                raise RuntimeError(f"Error in process:\n{e}\nTrace:{trace}")

    async def run_script(self, execution_id: str, already_in_sub_process: bool = False):
        script_context.set(ScriptExecutionContext(script_id=self.script_id, execution_id=execution_id))
        async with self.guard("Get script execution info"):
            script_report = await self.script_history_cache.get(execution_id)
        async with self.guard("Script collection"):
            script = await self.collector.collect_script_by_id(self.script_id, script_report.root_folder)
            script_context.set(
                ScriptExecutionContext(
                    script_id=self.script_id, execution_id=execution_id, min_step_level=script.callable.min_step_level
                )
            )
        if script.callable.memory_intensive and not already_in_sub_process:
            await self.run_script_in_sub_process(execution_id)
        else:
            async with self.guard("Prime environment context"):
                env.prime_environment(
                    env_name=script_report.env_name,
                    setting_overwrite=script_report.setting_overwrite,
                    env_user_contexts=[script_context],
                )
            async with self.guard("Validate input script parameters"):
                input_params = self.collector.process_input_params(script.params, script_report.params)
                input_params_for_save = self.collector.process_input_params_for_save(
                    script.params, script_report.params, input_params
                )
                await self.script_history_cache.update(execution_id, ScriptHistoryUpdate(params=input_params_for_save))
            try:
                result = await self._run_script_function(script, input_params, execution_id)
            except Exception as e:
                await self.reporter.finish_script_report_with_error(
                    execution_id=execution_id, error=e, context=script_context.get()
                )
            else:
                await self.reporter.finish_script_report(
                    execution_id=execution_id, result=result, context=script_context.get()
                )


def run_memory_intensive_script_in_process(script_id: str, execution_id: str, conn: Pipe):
    try:
        engine = create_async_engine(settings.SQLALCHEMY_ASYNC_DATABASE_URI, pool_pre_ping=True)
        process_db_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        asyncio.run(ScriptManager(script_id, process_db_session).run_script(execution_id, already_in_sub_process=True))
        conn.send(None)
    except Exception as e:
        conn.send((e, traceback.format_exc()))
    finally:
        conn.close()
