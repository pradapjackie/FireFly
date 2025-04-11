from src.cache.base_collected_cache import BaseTestCache
from src.schemas.load_test.load_test import CollectedLoadTest


class LoadTestCache(BaseTestCache):
    def __init__(self):
        super().__init__(key="collected_load_tests", return_model=CollectedLoadTest)
