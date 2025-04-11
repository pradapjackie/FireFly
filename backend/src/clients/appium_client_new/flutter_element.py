from src.clients.appium_client_new.flutter_id_generator import FlutterElementId
from src.clients.appium_client_new.schemas.requests_and_responses import SendTextRequest
from src.modules.auto_test.step_manager import step


class FlutterElement:
    def __init__(self, session, element_id: FlutterElementId):
        self.session = session
        self.element_id = element_id

    async def click(self):
        async with step("Click element"):
            await self.session.post(f"session/{self.session.session_id}/element/{self.element_id}/click")

    async def send_keys(self, text: str):
        async with step("Send keys to element"):
            data = SendTextRequest(text=text)
            await self.session.post(f"session/{self.session.session_id}/element/{self.element_id}/value", json=data)

    async def wait_for_presence(self, seconds_timeout: int = 10):
        async with step("Wait for element presence"):
            await self.session.execute_script("flutter:waitFor", [self.element_id, seconds_timeout * 1000])

    async def wait_for_tappable(self):
        async with step("Wait for element tappable"):
            await self.session.execute_script("flutter:waitForTappable", [self.element_id])

    async def get_text(self) -> str:
        async with step("Get element text"):
            result = await self.session.get(f"session/{self.session.session_id}/element/{self.element_id}/text")
            return result["value"]
