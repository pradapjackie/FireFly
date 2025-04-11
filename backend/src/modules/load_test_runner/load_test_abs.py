from abc import ABC, abstractmethod


class LoadTestAbc(ABC):
    """"""

    class Config:
        maximum_number_of_workers = 10
        concurrency_within_a_single_worker = 20

    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def worker(self):
        pass

    @abstractmethod
    async def teardown(self):
        pass
