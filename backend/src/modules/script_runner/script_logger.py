from src.modules.script_runner.contexts import script_context
from src.modules.script_runner.reporter import Reporter


async def log(*args):
    context = script_context.get()
    await Reporter(context.script_id).add_log(context.execution_id, " ".join([str(arg) for arg in args]))
