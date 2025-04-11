from typing import Any, List

from pydantic import BaseModel

from src.clients.appium_client_new.schemas.capabilities import Capabilities, CreatedSessionCapabilities
from src.utils.pydantic_helper import BaseResponse, CamelCaseModel, CamelCaseResponse, all_optional


class CreateSessionRequest(CamelCaseModel):
    capabilities: Capabilities


class CreateSessionResponse(CamelCaseResponse):
    capabilities: CreatedSessionCapabilities
    session_id: str


@all_optional
class StopSessionResponse(BaseResponse):
    state: str
    status: int
    value: str | None = None


class SendTextRequest(BaseModel):
    value: List[str] | None = None
    text: str | None = None


class ExecuteScriptRequest(BaseModel):
    script: str
    args: List[Any]
