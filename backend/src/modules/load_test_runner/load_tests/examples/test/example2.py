from src.modules.load_test_runner.load_test_abs import LoadTestAbc


class Example2LoadTest(LoadTestAbc):
    async def setup(self):
        pass

    async def worker(self):
        pass

    async def teardown(self):
        pass
