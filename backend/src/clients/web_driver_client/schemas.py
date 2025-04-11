from asyncio import Semaphore
from typing import Dict, List

from pydantic import BaseModel, ConfigDict

from src.clients.web_driver_client.session import WebSession


class VmHostConfig(BaseModel):
    url: str
    description: str
    max_sessions: Semaphore

    model_config = ConfigDict(arbitrary_types_allowed=True)


class VmHosts(BaseModel):
    vm_list: List[VmHostConfig]
    localhost: VmHostConfig


class WebConfig(BaseModel):
    hosts: VmHosts
    capabilities: Dict


class WebSessionContext(BaseModel):
    web_session: WebSession
    host: VmHostConfig

    model_config = ConfigDict(arbitrary_types_allowed=True)
