import json
from contextvars import ContextVar
from typing import Dict, List

import redis
from redis.asyncio import Redis

from src import crud
from src.core.config import settings
from src.modules.environment.default import REPLACE_THIS, DefaultEnv
from src.schemas.environment import EnvEnum, EnvOverwriteParam, EnvUserContext


class Environment(DefaultEnv):
    def __init__(self):
        self._primed = False
        self.env_name: EnvEnum | None = None
        self._overwrite: Dict[str, EnvOverwriteParam] | None = None
        self._env_user_contexts: List[ContextVar[EnvUserContext]] | None = None
        self._env_user_multi_contexts: List[ContextVar[List[EnvUserContext]]] | None = None
        self._redis = redis.from_url(settings.REDIS_CACHE)
        self._reserved = ("prime_environment", "prefix", "env_name")
        self.prefix = "ENV_VARIABLE_"
        super().__init__()

    def prime_environment(
        self,
        env_name: EnvEnum,
        setting_overwrite: Dict[str, EnvOverwriteParam],
        env_user_contexts: List[ContextVar[EnvUserContext]] | None = None,
        env_user_multi_contexts: List[ContextVar[List[EnvUserContext]]] | None = None,
    ):
        self.env_name = env_name
        self._overwrite = setting_overwrite
        self._env_user_contexts = env_user_contexts or []
        self._env_user_multi_contexts = env_user_multi_contexts or []
        self._primed = True

    def __getattribute__(self, name) -> str:
        if name.startswith("_") or name in self._reserved:
            return super().__getattribute__(name)

        if self._primed:
            if found_overwrite := self._overwrite.get(name):
                result, secure = found_overwrite.value, found_overwrite.secure
            elif found_item := self._redis.hget(f"env:{self.env_name}", name):
                item = EnvOverwriteParam(**json.loads(found_item.decode("UTF-8")))
                result, secure = item.value, item.secure
            else:
                result, secure = super().__getattribute__(name), False
                if result == REPLACE_THIS:
                    raise KeyError(f"It is necessary to fill in the value of {name} in the environment settings")
        else:
            result, secure = self.prefix + name, False

        if self._env_user_contexts:
            for context in self._env_user_contexts:
                if context and context.get(None):
                    context_value = context.get()
                    context_value.env_used[name] = str(result) if not secure else "******"

        if self._env_user_multi_contexts:
            for multi_context in self._env_user_multi_contexts:
                if multi_context and multi_context.get(None):
                    for context in multi_context.get():
                        context.env_used[name] = str(result) if not secure else "******"

        return result


async def prime_environment_cache(db, aio_redis: Redis):
    data_from_db = await crud.auto_test_env.get_multi(db)
    for item in data_from_db:
        await aio_redis.hset(f"env:{item.env}", item.param, json.dumps({"value": item.value, "secure": item.secure}))
    for env_name in EnvEnum.list():
        data_from_redis = await aio_redis.hgetall(f"env:{env_name}")
        for param in data_from_redis.keys():
            if not any(item for item in data_from_db if item.param == param.decode("UTF-8")):
                await aio_redis.hdel(f"env:{env_name}", param)


env = Environment()
