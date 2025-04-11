from abc import ABC, abstractmethod
from typing import Any

from src.cache.base import CacheBase
from src.cache.load_test.public_event_channel import LoadTestPublicEventChannel


class LoadTestChartsCache(CacheBase[Any, Any], ABC):
    def __init__(self):
        self.channel = LoadTestPublicEventChannel()
        super().__init__()

    @abstractmethod
    async def get_chart_data(self, load_test_id: str, execution_id: str, chart_name: str) -> Any:
        pass
