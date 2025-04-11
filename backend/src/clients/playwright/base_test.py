from contextvars import ContextVar

from playwright.async_api import Browser, Page, Playwright, PlaywrightContextManager, async_playwright
from pydantic import BaseModel, ConfigDict

from src.modules.auto_test.test_abs import TestAbs
from src.modules.auto_test.utils.assets_helper import AssetsHelper
from src.utils.dynamic_form import CheckboxFiled


class WebTestContext(BaseModel):
    browser: Browser

    model_config = ConfigDict(arbitrary_types_allowed=True)


web_test_context: ContextVar[WebTestContext] = ContextVar("web_test_context")


class BasePlaywrightTest(TestAbs):
    class RunConfig:
        execute_on_local = CheckboxFiled(label="Execute test on local Playwright server")

    assets_helper: AssetsHelper | None = None
    playwright_context: PlaywrightContextManager | None = None
    session: Playwright | None = None

    def __init__(self):
        self.browser: Browser | None = None
        self._current_page: Page | None = None

    @classmethod
    async def group_setup(cls):
        cls.playwright_context = async_playwright()
        cls.session = await cls.playwright_context.start()
        cls.assets_helper = AssetsHelper()

    async def setup(self, **test_params):
        playwright_server_domain = "host.docker.internal" if self.RunConfig.execute_on_local.value else "playwright"
        playwright_server_port = "49240" if self.RunConfig.execute_on_local.value else "3010"
        self.browser = await self.session.chromium.connect(f"ws://{playwright_server_domain}:{playwright_server_port}/")
        web_test_context.set(WebTestContext(browser=self.browser))

    async def new_page(self) -> Page:
        page = await self.browser.new_page()
        self._current_page = page
        return page

    @staticmethod
    async def enable_semantic(page: Page):
        enable_semantic_button = page.locator("//flt-semantics-placeholder")
        await enable_semantic_button.wait_for(state="attached")
        await enable_semantic_button.dispatch_event("click")
        await page.locator("//flt-semantics-container[*[@aria-label or @role]]").first.wait_for(state="attached")

    async def teardown(self, **test_params):
        if self._current_page:
            screenshot_bytes = await self._current_page.screenshot()
            await self.assets_helper.add_image("Screenshot after completion", screenshot_bytes)
        await self.browser.close()

    @classmethod
    async def group_teardown(cls):
        cls.assets_helper and await cls.assets_helper.close_connection()
        cls.playwright_context and await cls.playwright_context.__aexit__()
