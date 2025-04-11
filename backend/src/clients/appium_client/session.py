from base64 import b64decode
from typing import List, Optional

from yarl import URL

from src.clients.appium_client import schemas
from src.clients.appium_client.appium_http_client import AppiumHttpClient
from src.clients.appium_client.schemas.element import ActionsChain, ExecuteScriptPayload
from src.clients.appium_client.schemas.session import TerminateAppBody
from src.modules.auto_test.step_manager import step
from src.modules.environment.env import env
from src.utils.rate_limiter import RedisRateLimiter


class AppiumSessionLimiter(RedisRateLimiter):
    pass


class Session:
    def __init__(self, hub_url: URL, user: str, password: str, **transport_kwargs):
        self.appium_url = hub_url.with_user(user).with_password(password)
        self.appium_client = AppiumHttpClient(self.appium_url, session_exception_callback=self.stop, **transport_kwargs)

        self.id: Optional[str] = None
        self.real_capabilities: Optional[schemas.NewSessionCapabilities] = None

        self.limit = AppiumSessionLimiter(
            int(env.appium_session_limit), timeout=int(env.appium_session_acquire_timeout)
        )

    @property
    def started(self) -> bool:
        return bool(self.id)

    async def start(self, capabilities: schemas.DesiredCapabilities):
        await self.limit.acquire()
        try:
            self.id = await self._start(capabilities)
        except Exception as e:
            await self.limit.release()
            raise RuntimeError(f"Failed to create session: {e}") from e

    async def stop(self):
        if self.id:
            try:
                session_to_close = self.id
                self.id = None
                await self.limit.release()
                await self._stop(session_to_close)
            except Exception as e:
                raise RuntimeError(f"Failed to stop session: {e}") from e
        await self.appium_client.close()

    async def _start(self, capabilities: schemas.DesiredCapabilities) -> str:
        async with step("Start Appium session"):
            data = schemas.CreateSessionRequest(capabilities=schemas.Capabilities(always_match=capabilities))
            result = await self.appium_client.start_session(data)
            self.real_capabilities = result.capabilities
            return result.session_id

    async def _stop(self, session_id):
        async with step("Stop Appium session"):
            await self.appium_client.stop_session(session_id)

    async def get_window_rect(self) -> schemas.WindowRect:
        return await self.appium_client.get_window_rect(self.id)

    async def get_source(self) -> str:
        async with step("Getting app source"):
            return await self.appium_client.get_source(self.id)

    async def terminate_app(self):
        async with step("Terminating app"):
            t = TerminateAppBody(bundle_id=self.real_capabilities.bundle_id, app_id=self.real_capabilities.app_package)
            await self.appium_client.terminate_app(self.id, t)

    async def activate_app(self):
        async with step("Activating app"):
            t = TerminateAppBody(bundle_id=self.real_capabilities.bundle_id, app_id=self.real_capabilities.app_package)
            await self.appium_client.activate_app(self.id, t)

    async def get_screenshot(self) -> bytes:
        result = await self.appium_client.get_screenshot(self.id)
        return b64decode(result.encode("ascii"))

    async def execute_script(self, command: str, arguments: List[dict]):
        await self.appium_client.execute_script(self.id, ExecuteScriptPayload(script=command, args=arguments))

    async def execute_actions_chain(self, actions: ActionsChain):
        await self.appium_client.execute_actions(self.id, actions)
