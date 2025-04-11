import asyncio
import inspect
from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.cache.script_runner.script_cache import ScriptCollectedCache
from src.cache.script_runner.script_paths import ScriptPathsCache
from src.modules.base_collector import BaseCollector
from src.modules.script_runner.config import settings
from src.modules.script_runner.register import register
from src.modules.script_runner.script_class_abs import ScriptClassAbc
from src.schemas.common import CollectObjectTypes
from src.schemas.script_runner.script import CollectedScript, RegisteredScript, Script, ScriptDB
from src.utils.dynamic_form import Field
from src.utils.format import format_class_or_method_name
from src.utils.rate_limiter import RedisLock


class Collector(BaseCollector):
    def __init__(self):
        self.path_cache = ScriptPathsCache()
        self.collected_cache = ScriptCollectedCache()

    @staticmethod
    def get_script_signature_parameters(script: RegisteredScript) -> List[inspect.Parameter]:
        if script.is_class:
            return list(inspect.signature(script.callable.run).parameters.values())[1:]
        elif script.is_coroutine or script.is_async_generator:
            return list(inspect.signature(script.callable).parameters.values())
        else:
            raise NotImplementedError(
                f"Script {script.name} type is not supported. "
                f"The script must be an asynchronous function or async generator "
                f"or a child of the {ScriptClassAbc.__class__.__name__} class."
            )

    @staticmethod
    def get_script_doc_string(script: RegisteredScript) -> str:
        if script.is_class:
            return inspect.getdoc(script.callable.run)
        elif script.is_coroutine or script.is_async_generator:
            return inspect.getdoc(script.callable)
        else:
            raise NotImplementedError(
                f"Script {script.name} type is not supported. "
                f"The script must be an asynchronous function or async generator "
                f"or a child of the {ScriptClassAbc.__class__.__name__} class."
            )

    def get_script_parameters(self, script: RegisteredScript) -> Dict[str, Field]:
        signature_parameters = self.get_script_signature_parameters(script)
        return self.signature_to_params(script.name, signature_parameters)

    async def collect_scripts(self, root_folder: str | None = None) -> List[Script]:
        async with RedisLock(name="Script collection", timeout=60 * 10):
            collected_root_folders = self.collect_root_folders(root_path=settings.ROOT_PATH)
            collected_scripts: List[RegisteredScript] = await self.collect(
                root_path=settings.ROOT_PATH,
                acceptable_types_of_objects=[CollectObjectTypes.class_, CollectObjectTypes.async_function],
                collected_type=RegisteredScript,
                decorator=register,
                root_folder=root_folder,
            )
            scripts = [
                Script(**collected_script.model_dump(), params=self.get_script_parameters(collected_script))
                for collected_script in collected_scripts
            ]
            await self.path_cache.save_root_folders(collected_root_folders)
            await self.path_cache.save_paths(scripts)
            return scripts

    async def get_collected_folders(self) -> List[str]:
        return await self.path_cache.get_root_folders()

    async def collect_script_by_id(self, script_id: str, root_folder: str) -> Script:
        script_path, script_name = await self.path_cache.get(script_id, root_folder)
        collected_script = self.import_from_file(
            root_path=settings.ROOT_PATH,
            file_path=script_path,
            object_name=script_name,
            collected_type=RegisteredScript,
        )
        return Script(**collected_script.model_dump(), params=self.get_script_parameters(collected_script))

    async def collect_and_save_scripts_in_db(self, db: AsyncSession, root_folder: str | None = None) -> None:
        collected_scripts = await self.collect_scripts(root_folder=root_folder)
        scripts_to_save = []
        for script in collected_scripts:
            scripts_to_save.append(
                ScriptDB(
                    id=script.id,
                    name=script.name,
                    display_name=format_class_or_method_name(script.name),
                    description=self.get_script_doc_string(script),
                    root_folder=script.root_folder,
                    filepath=".".join([*script.path.parts[1:-1], script.path.stem]),
                    params=script.params,
                )
            )
        await crud.script.save_scripts(db, scripts_to_save)

    async def get_collected_scripts(self, db: AsyncSession, root_folder: str) -> List[CollectedScript]:
        if result := await self.collected_cache.get_list(root_folder):
            return result

        scripts = await crud.script.get_scripts(db, root_folder)
        result = [CollectedScript.model_validate(script) for script in scripts]

        if result:
            await self.collected_cache.save(root_folder, result)

        return result

    async def prime_collected_cache(self, db: AsyncSession):
        for root_folder in await self.path_cache.get_root_folders():
            await self.get_collected_scripts(db, root_folder)

    async def clear_collected_scripts_cache(self):
        folders = await self.path_cache.get_root_folders()
        await asyncio.gather(*[self.collected_cache.delete(root_folder) for root_folder in folders])

    @staticmethod
    async def get_script_by_id(db: AsyncSession, script_id: str) -> ScriptDB:
        script = await crud.script.get(db, script_id)
        if not script:
            raise HTTPException(404, f"No such script: {script_id}")
        return ScriptDB.model_validate(script)
