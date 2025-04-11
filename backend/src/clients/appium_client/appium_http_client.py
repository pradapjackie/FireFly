import uuid
from typing import Callable, List, Optional

from aiohttp import BasicAuth, TCPConnector
from pydantic import BaseModel
from yarl import URL

from src.clients.appium_client import schemas
from src.clients.appium_client.errors import check_response_error
from src.clients.appium_client.schemas import ActionsChain
from src.clients.appium_client.schemas.element import ExecuteScriptPayload
from src.clients.appium_client.schemas.session import TerminateAppBody
from src.clients.http_client.client import HttpClient


class AppiumHttpClient(HttpClient):
    def __init__(self, base_url: URL, session_exception_callback: Callable, **kwargs):
        super().__init__(base_url, **kwargs, auth=BasicAuth.from_url(base_url), connector=TCPConnector(ssl=False))
        self.error_callback = session_exception_callback
        self.base_prefix = URL("/wd/hub")

    @staticmethod
    def _get_connection_headers():
        return {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "appium/python 2.6.0 (selenium/4.4.0 (python windows))",
            "Connection": "keep-alive",
            "X-Idempotency-Key": str(uuid.uuid4()),
        }

    async def request(self, method: str, url: str, data: Optional[BaseModel] = None) -> dict:
        data = data.model_dump(by_alias=True, exclude_none=True) if data else None
        async with self.http_session.request(
            method=method, url=self.base_prefix / url, json=data, headers=self._get_connection_headers()
        ) as resp:
            if url == "session":
                response = await resp.read()
                print(f"Session start response: {resp.status} {response.decode()}")
            result = await resp.json()
            await check_response_error(status=resp.status, data=result, session_exception_callback=self.error_callback)
            return result

    async def start_session(self, data: schemas.CreateSessionRequest) -> schemas.Session:
        result = await self.request("POST", "session", data=data)
        return schemas.Session(**result["value"])

    async def stop_session(self, session_id: str) -> schemas.StopSessionResponse:
        result = await self.request("DELETE", f"session/{session_id}")
        return schemas.StopSessionResponse(**result)

    async def close(self):
        await self.http_session.close()

    async def terminate_app(self, session_id: str, data: TerminateAppBody):
        await self.request("POST", f"session/{session_id}/appium/device/terminate_app", data=data)

    async def activate_app(self, session_id: str, data: TerminateAppBody):
        await self.request("POST", f"session/{session_id}/appium/device/activate_app", data=data)

    async def get_window_rect(self, session_id: str) -> schemas.WindowRect:
        result = await self.request("GET", f"session/{session_id}/window/rect")
        return schemas.WindowRect(**result["value"])

    async def get_source(self, session_id: str) -> str:
        result = await self.request("GET", f"session/{session_id}/source")
        return result["value"]

    async def execute_actions(self, session_id: str, actions: ActionsChain):
        await self.request("POST", f"session/{session_id}/actions", data=actions)

    async def execute_script(self, session_id: str, script_payload: ExecuteScriptPayload):
        await self.request("POST", f"session/{session_id}/execute/sync", data=script_payload)

    async def find_element(self, session_id: str, data: schemas.FindElementRequest) -> schemas.Element:
        result = await self.request("POST", f"session/{session_id}/element", data=data)
        return schemas.Element(**result["value"])

    async def find_child_element(
        self, session_id: str, element_id: str, data: schemas.FindChildElementRequest
    ) -> schemas.Element:
        result = await self.request("POST", f"session/{session_id}/element/{element_id}/element", data=data)
        return schemas.Element(**result["value"])

    async def find_elements(self, session_id: str, data: schemas.FindElementRequest) -> List[schemas.Element]:
        result = await self.request("POST", f"session/{session_id}/elements", data=data)
        return list(map(lambda v: schemas.Element(**v), result["value"]))

    async def send_text(self, session_id: str, element_id: str, data: schemas.SendTextRequest):
        await self.request("POST", f"session/{session_id}/element/{element_id}/value", data=data)

    async def click(self, session_id: str, element_id: str):
        await self.request("POST", f"session/{session_id}/element/{element_id}/click")

    async def get_text(self, session_id: str, element_id: str) -> str:
        result = await self.request("GET", f"session/{session_id}/element/{element_id}/text")
        return result["value"]

    async def is_element_visible(self, session_id: str, element_id: str) -> bool:
        result = await self.request("GET", f"session/{session_id}/element/{element_id}/displayed")
        return result["value"]

    async def get_location(self, session_id: str, element_id: str) -> schemas.ElementLocation:
        result = await self.request("GET", f"session/{session_id}/element/{element_id}/location")
        return schemas.ElementLocation(**result["value"])

    async def get_size(self, session_id: str, element_id: str) -> schemas.ElementSize:
        result = await self.request("GET", f"session/{session_id}/element/{element_id}/size")
        return schemas.ElementSize(**result["value"])

    async def get_attribute(self, session_id: str, element_id: str, attribute_name: str) -> str:
        result = await self.request("GET", f"session/{session_id}/element/{element_id}/attribute/{attribute_name}")
        return result["value"]

    async def get_screenshot(self, session_id: str) -> str:
        result = await self.request("GET", f"session/{session_id}/screenshot")
        return result["value"]
