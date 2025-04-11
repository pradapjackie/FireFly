from src.cache.base_path_cache import BasePathsCache


class ScriptPathsCache(BasePathsCache):
    def __init__(self):
        super().__init__(module_name="script")
