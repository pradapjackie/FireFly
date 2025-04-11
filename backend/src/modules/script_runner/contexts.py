from contextvars import ContextVar
from typing import Optional

from pydantic import ConfigDict

from src.schemas.auto_test.common import StepLevel
from src.schemas.environment import EnvUserContext


class ScriptExecutionContext(EnvUserContext):
    script_id: str
    execution_id: str
    min_step_level: StepLevel = StepLevel.info

    model_config = ConfigDict(arbitrary_types_allowed=True)


script_context: ContextVar[Optional[ScriptExecutionContext]] = ContextVar("script_context")
