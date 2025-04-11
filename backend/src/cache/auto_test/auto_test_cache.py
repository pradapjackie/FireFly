from src.cache.base_collected_cache import BaseTestCache
from src.schemas.auto_test.auto_test import CollectedTestsResponse


class AutoTestCache(BaseTestCache):
    def __init__(self):
        super().__init__(key="collected_auto_tests", return_model=CollectedTestsResponse)
