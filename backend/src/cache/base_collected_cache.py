import json
from typing import Generic, List, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.cache.base import CacheBase
from src.core.config import settings as app_settings

CollectedType = TypeVar("CollectedType")


class BaseTestCache(CacheBase, Generic[CollectedType]):
    def __init__(self, key: str, return_model: Type[BaseModel]):
        self.root_key = f"{key}:{app_settings.PROJECT_VERSION}"
        self.return_model = return_model
        super().__init__()

    async def save(self, root_folder: str, cached_response: CollectedType):
        await self._create_key(f"{self.root_key}:{root_folder}", json.dumps(jsonable_encoder(cached_response)))

    async def get(self, root_folder: str) -> CollectedType | None:
        result = await self._get_key(f"{self.root_key}:{root_folder}")
        if result:
            return self.return_model.model_validate_json(result)

    async def get_list(self, root_folder: str) -> List[CollectedType] | None:
        result = await self._get_key(f"{self.root_key}:{root_folder}")
        if result:
            return [self.return_model.model_validate(item) for item in json.loads(result)]

    async def delete(self, root_folder: str):
        await self._delete_key(f"{self.root_key}:{root_folder}")
