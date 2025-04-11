import asyncio
import random

from src.modules.auto_test.register import params, register
from src.modules.auto_test.step_manager import step
from src.modules.auto_test.test_abs import TestAbs


@register()
class Long(TestAbs):
    @params(
        [
            dict(iteration_name="First"),
            dict(iteration_name="Second"),
            dict(iteration_name="Third"),
        ]
    )
    async def test_success(self):
        async with step("First wait"):
            await asyncio.sleep(random.randrange(5, 20))
        async with step("Second wait"):
            await asyncio.sleep(random.randrange(5, 20))
        async with step("Third wait"):
            await asyncio.sleep(random.randrange(5, 20))


@register()
class Longer(TestAbs):
    @params(
        [
            dict(iteration_name="First"),
            dict(iteration_name="Second"),
            dict(iteration_name="Third"),
        ]
    )
    async def test_success(self):
        async with step("First wait"):
            await asyncio.sleep(random.randrange(20, 60))
        async with step("Second wait"):
            await asyncio.sleep(random.randrange(20, 60))
        async with step("Third wait"):
            await asyncio.sleep(random.randrange(20, 60))
