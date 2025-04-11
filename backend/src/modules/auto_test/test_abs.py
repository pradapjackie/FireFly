from abc import ABC
from typing import List


class TestAbs(ABC):
    @classmethod
    async def group_setup(cls):
        pass

    async def setup(self, **test_params):
        pass

    async def teardown(self, **test_params):
        pass

    @classmethod
    async def group_teardown(cls):
        pass

    tags: List[str] | None = None
