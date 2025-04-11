from src.modules.auto_test.step_manager import StepLevel
from src.schemas.script_runner.script import ScriptCallableType


def register(
    script_callable: ScriptCallableType | None = None,
    *,
    min_step_level: StepLevel = StepLevel.info,
    memory_intensive: bool = False,
):
    def decorator(inner_script_callable: ScriptCallableType):
        inner_script_callable.min_step_level = min_step_level
        inner_script_callable.memory_intensive = memory_intensive
        return inner_script_callable

    # Decorator used with parameter
    if script_callable is None:
        return decorator
    # Decorator used without parameter
    else:
        return decorator(script_callable)
