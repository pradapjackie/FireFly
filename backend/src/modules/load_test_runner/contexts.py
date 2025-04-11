from contextvars import ContextVar
from typing import Optional

from pydantic import ConfigDict

from src.schemas.environment import EnvUserContext


class LoadTestExecutionContext(EnvUserContext):
    load_test_id: str
    execution_id: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


load_test_context: ContextVar[Optional[LoadTestExecutionContext]] = ContextVar("load_test_context")
