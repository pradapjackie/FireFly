import inspect
from typing import Any, Awaitable, Callable, Dict, Type

from pydantic import BaseModel, ConfigDict

from src.core.config import settings
from src.modules.script_runner.script_class_abs import ScriptClassAbc
from src.schemas.common import CollectedObject
from src.schemas.environment import EnvEnum, EnvOverwriteParam
from src.utils.dynamic_form import Field
from src.utils.hash_funcs import md5

FuncScriptType = Callable[[Any, Any], Awaitable[Any]]
ClassScriptType = Type[ScriptClassAbc]
ScriptCallableType = FuncScriptType | ClassScriptType


class RegisteredScript(CollectedObject):
    callable: ScriptCallableType

    @property
    def is_class(self) -> bool:
        return inspect.isclass(self.callable) and issubclass(self.callable, ScriptClassAbc)

    @property
    def is_class_with_async_generator(self) -> bool:
        return self.is_class and inspect.isasyncgenfunction(self.callable.run)

    @property
    def is_coroutine(self) -> bool:
        return inspect.iscoroutinefunction(self.callable)

    @property
    def is_async_generator(self) -> bool:
        return inspect.isasyncgenfunction(self.callable)

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.callable)


class Script(RegisteredScript):
    params: Dict[str, Field]

    @property
    def id(self) -> str:
        prefix = "".join(c for c in self.name if c.isalpha() or c == "_")
        params_hash = md5("".join([str(self.path), str(self.params)]))
        return prefix + params_hash


class ScriptDB(BaseModel):
    id: str
    name: str
    display_name: str
    description: str | None = None
    root_folder: str
    filepath: str
    params: Dict
    supported_from: str = settings.PROJECT_VERSION
    supported_to: str = settings.PROJECT_VERSION

    model_config = ConfigDict(from_attributes=True)


class CollectedScript(BaseModel):
    id: str
    display_name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class StartScriptRequest(BaseModel):
    root_folder: str
    env_name: EnvEnum
    setting_overwrite: Dict[str, EnvOverwriteParam]
    script_id: str
    params: Dict


class StartScriptResponse(BaseModel):
    execution_id: str
