from enum import StrEnum
from typing import Dict, List, Self

from pydantic import BaseModel, ConfigDict

from src.utils.pydantic_helper import all_optional


class EnvEnum(StrEnum):
    dev = "dev"
    trunk = "trunk"
    staging = "staging"
    prod = "prod"

    @classmethod
    def list(cls) -> List[Self]:
        return list(cls)


class AutoTestEnv(BaseModel):
    param: str
    env: EnvEnum
    value: str
    secure: bool

    model_config = ConfigDict(from_attributes=True)


@all_optional
class AutoTestEnvUpdate(AutoTestEnv):
    pass


class AutoTestEnvUpdateRequest(BaseModel):
    new: List[AutoTestEnv]
    removed: List[str]
    updated: List[AutoTestEnvUpdate]


class EnvOverwriteParam(BaseModel):
    value: str
    secure: bool


class EnvUserContext(BaseModel):
    env_used: Dict[str, str] = {}
