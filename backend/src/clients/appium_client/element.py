from __future__ import annotations

from typing import Optional, Tuple

from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    retry_if_not_exception_type,
    retry_if_result,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)

from src.clients.appium_client import errors, schemas
from src.clients.appium_client.action_chains_builder import ActionsBuilder
from src.clients.appium_client.appium_http_client import AppiumHttpClient
from src.clients.appium_client.unified_selector import UnifiedSelector
from src.clients.appium_client.use_session import UseSessionMixin
from src.modules.auto_test.step_manager import step


class BaseElement(UseSessionMixin):
    def __init__(self, element_id: Optional[str] = None):
        self.id = element_id

    @property
    def appium_client(self) -> AppiumHttpClient:
        return self.session.appium_client

    async def get_text(self) -> str:
        _id = await self._get_id()
        return await self.appium_client.get_text(self.session.id, _id)

    async def get_location(self) -> schemas.ElementLocation:
        _id = await self._get_id()
        return await self.appium_client.get_location(self.session.id, _id)

    async def get_size(self) -> schemas.ElementSize:
        _id = await self._get_id()
        return await self.appium_client.get_size(self.session.id, _id)

    async def send_text(self, text: str):
        _id = await self._get_id()
        data = schemas.SendTextRequest(text=text)
        await self.appium_client.send_text(self.session.id, _id, data)

    async def click(self):
        _id = await self._get_id()
        await self.appium_client.click(self.session.id, _id)

    async def find_element(self, selector: Tuple[schemas.By, str]) -> BaseElement:
        _id = await self._get_id()
        data = schemas.FindChildElementRequest(using=selector[0], value=selector[1], id=_id)
        result = await self.appium_client.find_child_element(self.session.id, _id, data)
        return BaseElement(result.id)

    async def _get_id(self) -> str:
        return self.id

    def reset(self):
        self.id = None

    def _reset_id(self, _):
        self.id = None

    async def _find(self) -> str:
        raise NotImplementedError

    async def _wait_for_element(self, retryer: Optional[AsyncRetrying] = None, timeout: Optional[int] = None):
        retryer = (
            retryer
            if retryer
            else AsyncRetrying(
                retry=retry_if_exception_type(errors.NoSuchElement),
                stop=(stop_after_delay(timeout if timeout else 20)),
                wait=wait_fixed(0.5),
                reraise=True,
            )
        )
        await retryer(self._find)

    async def _wait_for_element_absence(self, timeout: Optional[int] = None):
        acceptable_exceptions = (errors.NoSuchElement, errors.StaleElementReference)
        retryer = AsyncRetrying(
            retry=(
                retry_if_result(lambda value: isinstance(value, str))
                | retry_if_not_exception_type(acceptable_exceptions)
            ),
            stop=(stop_after_delay(timeout if timeout else 20)),
            wait=wait_fixed(0.5),
            reraise=True,
        )
        try:
            await retryer(self._find)
        except acceptable_exceptions:
            pass

    async def is_presented(self) -> bool:
        try:
            await self._find()
            return True
        except Exception as e:
            print(f"is_presented error is {str(e)}")
            return False

    async def is_presented_after_waiting(self, timeout: Optional[int] = None) -> bool:
        try:
            await self._wait_for_element(timeout=timeout)
            return True
        except Exception as e:
            print(f"is_presented_after_waiting error is {str(e)}")
            return False

    async def wait_for_invisibility(self, timeout: Optional[int] = None):
        await self._wait_for_element_absence(timeout)

    async def wait_for_presence(self, timeout: Optional[int] = None):
        await self._wait_for_element(timeout=timeout)

    async def get_attribute(self, attribute_name: str) -> str:
        _id = await self._get_id()
        result = await self.appium_client.get_attribute(self.session.id, _id, attribute_name)
        return result

    async def _click_with_retry(self, ignore_stale: bool):
        if ignore_stale:
            retryer = AsyncRetrying(
                retry=retry_if_exception_type((errors.NoSuchElement, errors.StaleElementReference)),
                stop=(stop_after_delay(20) | stop_after_attempt(40)),
                wait=wait_fixed(0.5),
                before_sleep=self._reset_id,
                reraise=True,
            )
        else:
            retryer = AsyncRetrying(
                retry=retry_if_exception_type(errors.NoSuchElement),
                stop=(stop_after_delay(20) | stop_after_attempt(40)),
                wait=wait_fixed(0.5),
                reraise=True,
            )
        await retryer(self.click)

    async def click_visible(self, ignore_stale: bool = False):
        await self._click_with_retry(ignore_stale)

    async def click_with_actions(self):
        await self.wait_for_visibility()
        size = await self.get_size()
        location = await self.get_location()
        x = int(size.width / 2) + location.x
        y = int(size.height / 2) + location.y
        actions = (
            ActionsBuilder().init_touch_actions().mouse_move(x, y, 250).pointer_down(0).pause(100).pointer_up(0).build()
        )
        await self.session.execute_actions_chain(actions)

    async def wait_for_visibility(self):
        retryer = AsyncRetrying(
            retry=retry_if_result(lambda value: value is False),
            stop=(stop_after_delay(20) | stop_after_attempt(40)),
            wait=wait_fixed(0.5),
            reraise=True,
        )
        await retryer(self.appium_client.is_element_visible, self.session.id, self.id)


class Element(BaseElement):
    def __init__(
        self,
        name: str | None = None,
        android_selector: Optional[Tuple[schemas.By, str]] = None,
        ios_selector: Optional[Tuple[schemas.By, str]] = None,
    ):
        super().__init__(None)
        self.selector = UnifiedSelector(android_selector, ios_selector)
        self.name = name if name else f"Unnamed element by selector: {self.selector[0]} {self.selector[1]}"

    @property
    def current_selector(self) -> UnifiedSelector:
        return self.selector

    async def _find(self) -> str:
        selector = self.current_selector
        data = schemas.FindElementRequest(using=selector[0], value=selector[1])
        result = await self.appium_client.find_element(self.session.id, data)
        self.id = result.id
        return result.id

    async def _get_id(self) -> str:
        if not self.id:
            await self._find()
        return self.id

    async def wait_for_visibility(self):
        await self.wait_for_presence()
        _id = await self._get_id()
        retryer = AsyncRetrying(
            retry=retry_if_result(lambda value: value is False),
            stop=(stop_after_delay(20) | stop_after_attempt(40)),
            wait=wait_fixed(0.5),
            reraise=True,
        )
        await retryer(self.appium_client.is_element_visible, self.session.id, _id)

    async def wait_for_presence_on_screen(self, screen_name: str, timeout: int | None = None):
        async with step(f"Check presence of {self.name} element on {screen_name}"):
            try:
                await self._wait_for_element(timeout=timeout)
            except Exception as e:
                raise AssertionError(f"{self.name} is not visible on the {screen_name}") from e


class DynamicElement(Element):
    def __init__(
        self,
        name: str | None = None,
        android_selector: Optional[Tuple[schemas.By, str]] = None,
        ios_selector: Optional[Tuple[schemas.By, str]] = None,
    ):
        super().__init__(name, android_selector, ios_selector)
        self._current_selector: UnifiedSelector = self.selector

    def set_dynamic_attrs(self, **kwargs):
        self._current_selector = self.selector.get_dynamic_selector(**kwargs)
        self.id = None

    @property
    def current_selector(self) -> UnifiedSelector:
        return self._current_selector
