from functools import partial
from typing import Any, Awaitable, Callable, List, Union

from arsenic import Session
from arsenic.connection import Connection
from arsenic.constants import WEB_ELEMENT
from arsenic.errors import NoSuchElement, WebdriverError
from arsenic.session import TCallback

from src.clients.web_driver_client.base_web_element import WebElement, WebSelector

TWaiter = Union[Callable[[int, TCallback], Awaitable[Any]], Callable[[int, TCallback, WebdriverError], Awaitable[Any]]]


class WebSession(Session):
    element_class = WebElement

    def __init__(self, connection: Connection, wait: TWaiter, driver, browser, bind: str = ""):
        super().__init__(connection, wait, driver, browser, bind)
        self.connection = connection
        self.bind = bind
        self.wait = wait
        self.driver = driver
        self.browser = browser

    async def get_element(self, selector: WebSelector, *args) -> WebElement:
        element = await super().get_element(selector.selector, selector.selector_type, *args)
        return self.element_class(element.id, element.connection, element.session)

    async def get_elements(self, selector: WebSelector, *args) -> List[WebElement]:
        elements = await super().get_elements(selector.selector, selector.selector_type, *args)
        return [self.element_class(element.id, element.connection, element.session) for element in elements]

    async def wait_for_element(self, timeout: int, selector: WebSelector, *args) -> WebElement:
        return await self.wait(
            timeout, partial(self.get_element, selector.selector, selector.selector_type, *args), NoSuchElement
        )

    async def wait_for_element_gone(self, timeout: int, selector: WebSelector, *args):
        async def callback():
            try:
                await self.get_element(selector, *args)
            except NoSuchElement:
                return True
            else:
                return False

        return await self.wait(timeout, callback)

    async def switch_to_frame(self, selector: WebSelector, *args):
        pure_frame = await super().get_element(selector.selector, selector.selector_type, *args)
        return await self._request(url="/frame", method="POST", data={"id": {WEB_ELEMENT: pure_frame.id}})
