from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.environment import EnvEnum, EnvOverwriteParam
from src.utils.pydantic_helper import all_optional


class ScriptStatusEnum(StrEnum):
    pending = "pending"
    success = "success"
    partial_success = "partial_success"
    fail = "fail"


class ScriptMultiResult(list):
    pass


class ScriptResultTypeEnum(StrEnum):
    string = "string"
    object = "object"
    table = "table"
    multi = "multi"
    file = "file"
    files = "files"


ToStringTypes = str | int | float | bool | bytes | date | datetime | None
ResultTypes = str | Dict[str, ToStringTypes] | List[Dict[str, ToStringTypes]]


class ScriptResult(BaseModel):
    type: ScriptResultTypeEnum
    object: Dict[int, ScriptResult] | List[ScriptResult] | ScriptFileResult | ResultTypes = Field(
        union_mode="left_to_right"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ScriptFileExtension(StrEnum):
    csv = "csv"


class ScriptFileResult(BaseModel):
    title: str
    type: ScriptFileExtension
    url: str


class ScriptError(BaseModel):
    name: str
    message: str
    traceback: str


class ScriptHistory(BaseModel):
    execution_id: str
    script_id: str
    params: Dict[str, str | int | float | bool | List[str | int | float] | date | Dict[str, str] | None] = {}
    status: ScriptStatusEnum = ScriptStatusEnum.pending
    root_folder: str
    env_name: EnvEnum
    setting_overwrite: Dict[str, EnvOverwriteParam] = {}
    env_used: Dict[str, str] = {}
    result: ScriptResult | None = None
    errors: List[ScriptError] | None = None
    user_id: int

    start_time: datetime
    end_time: datetime | None = None


class ScriptHistoryDB(BaseModel):
    id: str
    script_id: str
    params: Dict[str, str | int | float | bool | List[str | int | float] | None] = {}
    status: ScriptStatusEnum
    root_folder: str
    environment: EnvEnum
    env_used: Dict[str, str] = {}
    result_type: ScriptResultTypeEnum | None = None
    result: Dict[int, ScriptResult] | List[ScriptResult] | ScriptFileResult | ResultTypes = Field(
        union_mode="left_to_right"
    )
    errors: List[ScriptError] | None = None
    user_id: int
    start_time: str
    end_time: str


class ScriptHistoryItem(BaseModel):
    execution_id: str
    environment: EnvEnum
    status: ScriptStatusEnum
    result: ScriptResult | None = None
    errors: List[ScriptError] | None = None
    log: Dict[int, str] | None = None
    params: Dict[str, str | int | float | bool | List[str | int | float] | None] = {}
    env_used: Dict[str, str] = {}
    user_name: str
    start_time: datetime
    end_time: datetime


class ScriptHistoryDisplay(BaseModel):
    name: str
    history: List[ScriptHistoryItem]


@all_optional
class ScriptHistoryUpdate(ScriptHistory):
    pass


class ScriptFullHistory(ScriptHistory):
    log: Dict[int, str]
