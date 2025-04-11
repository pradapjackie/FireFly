from typing import Optional

from src.clients.web_driver_client.client import webdriver_client
from src.clients.web_driver_client.schemas import VmHostConfig, WebSessionContext
from src.clients.web_driver_client.session import WebSession
from src.clients.web_driver_client.web_session_context import web_session_context
from src.modules.auto_test.test_abs import TestAbs


class WebTest(TestAbs):
    def __init__(self, *args, **kwargs):
        self.web_session: Optional[WebSession] = None
        self.host: Optional[VmHostConfig] = None
        super().__init__(*args, **kwargs)

    async def setup(self, **test_params):
        self.web_session, self.host = await webdriver_client.get_session()
        web_session_context.set(WebSessionContext(web_session=self.web_session, host=self.host))

    async def teardown(self, **test_params):
        if self.web_session:
            await webdriver_client.close_session(self.web_session, self.host)
