import asyncio

from src.modules.script_runner.register import register
from src.modules.script_runner.script_class_abs import ScriptClassAbc


@register
async def i_am_coroutine_script():
    await asyncio.sleep(1)
    return "Coro"


@register
async def i_am_asynchronous_generator_script():
    await asyncio.sleep(1)
    yield "Async Gen"
    yield "Done"


@register
class IAmScriptClassWithCoroutine(ScriptClassAbc):
    async def run(self):
        await asyncio.sleep(1)
        return "Coro Class"


@register
class IAmScriptClassWithAsynchronousGenerator(ScriptClassAbc):
    async def run(self):
        await asyncio.sleep(1)
        yield "Async Gen Class"
        yield "Done"


@register(memory_intensive=True)
async def memory_intensive_script():
    await asyncio.sleep(1)
    return "Memory intensive Coro"
