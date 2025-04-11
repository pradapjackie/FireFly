from abc import ABC, abstractmethod


class ScriptClassAbc(ABC):
    @abstractmethod
    async def run(self, **kwargs):
        pass

    async def teardown(self, **kwargs):
        pass
