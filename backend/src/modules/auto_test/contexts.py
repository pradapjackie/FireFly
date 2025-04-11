from contextvars import ContextVar
from typing import List, Optional

from src.schemas.auto_test.auto_test import AutoTestContext
from src.schemas.auto_test.auto_test_history import Step
from src.schemas.auto_test.test_run import TestRun

test_run_context: ContextVar[TestRun] = ContextVar("test_run_context")
auto_test_context: ContextVar[Optional[AutoTestContext]] = ContextVar("test_case_id")
auto_test_contexts: ContextVar[Optional[List[AutoTestContext]]] = ContextVar("test_case_ids")
auto_test_current_step_list: ContextVar[Optional[List[Step]]] = ContextVar("auto_test_step_current")
