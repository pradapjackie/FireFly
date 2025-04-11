import asyncio
import random

from src.modules.load_test_runner.charts.boxplot import BoxPlot
from src.modules.load_test_runner.load_test_abs import LoadTestAbc


class ExampleLoadTest(LoadTestAbc):
    """Description"""

    class Config:
        maximum_number_of_workers = 18
        concurrency_within_a_single_worker = 2

    class Charts:
        time_of_requests = BoxPlot()

    def __init__(self, test: int = 5):
        print("init", flush=True)

    async def setup(self):
        await asyncio.sleep(random.randint(1, 5))
        print("setup", flush=True)

    async def worker(self):
        print("worker", flush=True)
        for i in range(100):
            print(f"From worker: {i}")
            await asyncio.sleep(random.randint(1, 5))
            await self.Charts.time_of_requests.update_box(random.randint(0, 100))

    async def teardown(self):
        await asyncio.sleep(random.randint(1, 5))
        print("teardown", flush=True)
