from base64 import b64decode
from typing import Any, List, Self

from src.clients.appium_client_new.appium_http_client import AppiumHttpClient
from src.clients.appium_client_new.flutter_element import FlutterElement
from src.clients.appium_client_new.flutter_id_generator import FlutterElementIdGenerator
from src.clients.appium_client_new.schemas.capabilities import Capabilities, DesiredCapabilities
from src.clients.appium_client_new.schemas.requests_and_responses import (
    CreateSessionRequest,
    CreateSessionResponse,
    ExecuteScriptRequest,
    StopSessionResponse,
)
from src.modules.auto_test.step_manager import step


class Session(AppiumHttpClient):
    def __init__(self):
        super().__init__(session_exception_callback=self.stop)
        self.session_id: str | None = None
        self.flutter_id_generator = FlutterElementIdGenerator()

    @property
    def started(self) -> bool:
        return bool(self.session_id)

    async def start(self, capabilities: DesiredCapabilities) -> Self:
        async with step("Start Appium session"):
            data = CreateSessionRequest(capabilities=Capabilities(always_match=capabilities))
            result = await self.post("session", json=data)
            response = CreateSessionResponse(**result["value"])
            self.session_id = response.session_id
            return self

    async def stop(self):
        async with step("Stop Appium session"):
            if self.session_id:
                result = await self.delete(f"session/{self.session_id}")
                self.session_id = None
                await self.close()
                return StopSessionResponse(**result)

    async def execute_script(self, script: str, script_arguments: List[Any] | None = None):
        async with step("Execute script"):
            request = ExecuteScriptRequest(script=script, args=script_arguments or [])
            return await self.post(f"session/{self.session_id}/execute/sync", json=request)

    def get_flutter_element_by_ancestor(
        self,
        ancestor: FlutterElement,
        matching: FlutterElement,
        match_root: bool = False,
        first_match_only: bool = False,
    ) -> FlutterElement:
        element_id = self.flutter_id_generator.by_ancestor(
            ancestor.element_id, matching.element_id, match_root, first_match_only
        )
        return FlutterElement(session=self, element_id=element_id)

    def get_flutter_element_by_descendant(
        self,
        descendant: FlutterElement,
        matching: FlutterElement,
        match_root: bool = False,
        first_match_only: bool = False,
    ) -> FlutterElement:
        element_id = self.flutter_id_generator.by_descendant(
            descendant.element_id, matching.element_id, match_root, first_match_only
        )
        return FlutterElement(session=self, element_id=element_id)

    def get_flutter_element_by_semantics_label(self, label: str, is_regexp: bool = False) -> FlutterElement:
        element_id = self.flutter_id_generator.by_semantics_label(label, is_regexp)
        return FlutterElement(session=self, element_id=element_id)

    def get_flutter_element_by_tooltip(self, text: str) -> FlutterElement:
        element_id = self.flutter_id_generator.by_tooltip(text)
        return FlutterElement(session=self, element_id=element_id)

    def get_flutter_element_by_text(self, text: str) -> FlutterElement:
        element_id = self.flutter_id_generator.by_text(text)
        return FlutterElement(session=self, element_id=element_id)

    def get_flutter_element_by_type(self, type_name: str) -> FlutterElement:
        element_id = self.flutter_id_generator.by_type(type_name)
        return FlutterElement(session=self, element_id=element_id)

    def get_flutter_element_by_value_key(self, key: str) -> FlutterElement:
        element_id = self.flutter_id_generator.by_value_key(key)
        return FlutterElement(session=self, element_id=element_id)

    async def wait_for_flutter_first_frame(self):
        async with step("Wait for first flatter frame"):
            await self.execute_script("flutter:waitForFirstFrame")

    async def get_screenshot(self) -> bytes:
        result = await self.get(f"session/{self.session_id}/screenshot")
        return b64decode(result["value"].encode("ascii"))
