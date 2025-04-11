import asyncio
from itertools import cycle
from typing import Tuple

from arsenic import browsers, services, start_session, stop_session
from arsenic.connection import Connection
from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from src.clients.web_driver_client.arsenic_monkey_patch import request as patched_request
from src.clients.web_driver_client.schemas import VmHostConfig, WebConfig
from src.clients.web_driver_client.session import WebSession
from src.clients.web_driver_client.vm_config import config
from src.modules.auto_test.utils.config_arsenic_log import __config_logger__
from src.modules.environment.env import env

__config_logger__()
Connection.request = patched_request


class WebdriverClient:
    def __init__(self):
        self.config: WebConfig = config
        self.browser = browsers.Chrome(**config.capabilities)
        self.browser.session_class = WebSession

    @retry(stop=(stop_after_delay(60) | stop_after_attempt(5)), wait=wait_fixed(1), reraise=True)
    async def _try_to_start_session(self, service) -> WebSession:
        return await start_session(service, self.browser)

    @retry(stop=(stop_after_delay(60) | stop_after_attempt(5)), wait=wait_fixed(1), reraise=True)
    async def _try_to_stop_session(self, session):
        await stop_session(session)

    async def choose_host(self) -> VmHostConfig:
        match env.selenium_server_config:
            case "localhost":
                return self.config.hosts.localhost
            case "vm_list":
                hosts = self.config.hosts.vm_list
                async with asyncio.Lock():
                    for i, host in enumerate(cycle(hosts)):
                        if not host.max_sessions.locked():
                            await host.max_sessions.acquire()
                            return host
                        else:
                            if (i + 1) % len(hosts) == 0:
                                await asyncio.sleep(5)
            case _:
                raise AttributeError(
                    f"Unknown selenium_server_config name: {env.selenium_server_config}. "
                    f"Possible values are: localhost and vm_list"
                )

    async def get_session(self) -> Tuple[WebSession, VmHostConfig]:
        host = await self.choose_host()
        service = services.Remote(url=host.url)
        session = await self._try_to_start_session(service)
        return session, host

    async def close_session(self, session, host: VmHostConfig):
        host.max_sessions.release()
        await self._try_to_stop_session(session)


webdriver_client = WebdriverClient()
