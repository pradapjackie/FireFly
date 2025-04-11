from asyncio import CancelledError
from functools import partial
from typing import Optional

from src.modules.auto_test.contexts import auto_test_current_step_list
from src.modules.script_runner.contexts import script_context
from src.modules.script_runner.script_logger import log
from src.schemas.auto_test.auto_test_history import StatusEnum
from src.schemas.auto_test.auto_test_history import Step as StepSchema
from src.schemas.auto_test.common import StepLevel


class Step:
    def __init__(self, step_name: str, *, step_level: StepLevel = StepLevel.info):
        self.step_name: str = step_name
        self.step_level: StepLevel = step_level
        self.auto_test_current_step = Optional[StepSchema]
        if self.in_auto_test_context:
            self.current_step_list: list = auto_test_current_step_list.get()
        if self.in_script_context:
            self.script_context = script_context.get(None)

    @property
    def in_auto_test_context(self) -> bool:
        return auto_test_current_step_list and auto_test_current_step_list.get(None) is not None

    @property
    def in_script_context(self) -> bool:
        return script_context and script_context.get(None) is not None

    async def __aenter__(self):
        if self.in_auto_test_context:
            self.auto_test_current_step = StepSchema(name=self.step_name, inner=[])
            self.current_step_list.append(self.auto_test_current_step)
            auto_test_current_step_list.set(self.auto_test_current_step.inner)
        if self.in_script_context and self.step_level >= script_context.get().min_step_level:
            await log(f"START STEP: {self.step_name}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.in_auto_test_context:
            if exc_type == CancelledError:
                # CancelledError exception can be often raised in tests due to coroutine cancellation.
                # It doesn't indicate that step failed - asyncio use this exception like a flag
                self.auto_test_current_step.status = StatusEnum.success
            else:
                self.auto_test_current_step.status = StatusEnum.success if not exc_type else StatusEnum.fail
            auto_test_current_step_list.set(self.current_step_list)
        if self.in_script_context and self.step_level >= script_context.get().min_step_level:
            await log(f"END STEP: {self.step_name}")


def step(step_name, *, step_level: StepLevel = StepLevel.info):
    return Step(step_name, step_level=step_level)


important_step = partial(step, step_level=StepLevel.important)
