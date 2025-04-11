from tenacity import AsyncRetrying, retry_if_result, stop_after_delay, wait_fixed
from yarl import URL

from src.clients.web_driver_client.session import WebSession
from src.clients.web_driver_client.web_session_context import web_session_context


class BasePage:
    def __init__(self, url: str | URL):
        self.url = url

    @property
    def web_session(self) -> WebSession:
        context = web_session_context.get()
        return context.web_session

    async def open(self):
        await self.web_session.get(str(self.url))

    async def get_page_state(self) -> str:
        return await self.web_session.execute_script("return document.readyState;")

    async def is_page_load(self) -> bool:
        page_url = await self.web_session.get_url()
        page_state = await self.get_page_state()
        return str(self.url) in page_url and page_state == "complete"

    async def wait_page_load(self, timeout=60, wait_between=0.5):
        retryer = AsyncRetrying(
            retry=retry_if_result(lambda value: value is False),
            stop=stop_after_delay(timeout),
            wait=wait_fixed(wait_between),
        )
        return await retryer(self.is_page_load)
