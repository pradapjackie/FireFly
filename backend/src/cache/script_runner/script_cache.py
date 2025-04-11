from src.cache.base_collected_cache import BaseTestCache
from src.schemas.script_runner.script import CollectedScript


class ScriptCollectedCache(BaseTestCache):
    def __init__(self):
        super().__init__(key="collected_scripts", return_model=CollectedScript)
