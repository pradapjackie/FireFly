from abc import ABC
from typing import Any

from src.cache.load_test.charts import LoadTestChartsCache
from src.modules.load_test_runner.contexts import load_test_context


class BaseChart(LoadTestChartsCache, ABC):
    def __init__(self):
        self.name = None
        super().__init__()

    @staticmethod
    def _get_execution_id() -> str:
        context = load_test_context.get()
        return context.execution_id

    @staticmethod
    def _get_load_test_id() -> str:
        context = load_test_context.get()
        return context.load_test_id

    async def send_update(self, data: Any):
        await self.channel.update_task_chart_data(self._get_load_test_id(), self._get_execution_id(), self.name, data)
