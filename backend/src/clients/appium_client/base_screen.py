import asyncio
from typing import Optional, Tuple

from src.clients.appium_client.action_chains_builder import ActionsBuilder
from src.clients.appium_client.base_test import mobile_test_context
from src.clients.appium_client.element import Element
from src.clients.appium_client.errors import AppiumError
from src.clients.appium_client.schemas import By, MobilePlatformEnum, ScrollDirection, ScrollToElementScript
from src.clients.appium_client.use_session import UseSessionMixin


class BaseScreen(UseSessionMixin):
    def __init__(self):
        self.unique_element: Optional[Element] = None

    @property
    def is_android(self) -> bool:
        return mobile_test_context.get().os == MobilePlatformEnum.android

    @property
    def is_ios(self) -> bool:
        return mobile_test_context.get().os == MobilePlatformEnum.ios

    async def is_page_open(self, timeout: int = None) -> bool:
        return await self.unique_element.is_presented_after_waiting(timeout=timeout)

    async def _swipe_to_element_ios(self, predicate_locator: Tuple[By, str]) -> bool:
        method, predicate = predicate_locator
        if method != By.IOS_PREDICATE:
            raise NotImplementedError(
                f"Swipe by script is only supported with predicate, but '{method}' was passed instead"
            )
        try:
            await self.session.execute_script(
                "mobile:scroll",
                [
                    ScrollToElementScript(
                        predicate_string=predicate, direction=ScrollDirection.down, to_visible=True
                    ).model_dump(by_alias=True)
                ],
            )
            if await Element(ios_selector=predicate_locator).is_presented():
                return True
        except Exception as e:
            print(f"ios top swipe to element exception: {e}")
        try:
            await self.session.execute_script(
                "mobile:scroll",
                [
                    ScrollToElementScript(
                        predicate_string=predicate, direction=ScrollDirection.up, to_visible=True
                    ).model_dump(by_alias=True)
                ],
            )
            return await Element(ios_selector=predicate_locator).is_presented()
        except Exception as e:
            print(f"ios down swipe to element exception: {e}")
            return False

    async def _swipe_to_element_android(
        self, automator_locator: Tuple[By, str], scrollable_selector: Tuple[By, str] = None
    ) -> bool:
        method, locator = automator_locator
        if method != By.ANDROID_UIAUTOMATOR:
            raise NotImplementedError(
                f"Swipe is only supported with automator locator, but '{method}' was passed instead"
            )
        try:
            return await Element(
                android_selector=(
                    By.ANDROID_UIAUTOMATOR,
                    f"new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView({locator})",
                )
                if scrollable_selector is None
                else (
                    By.ANDROID_UIAUTOMATOR,
                    f"new UiScrollable({scrollable_selector[1]}).scrollIntoView({locator})",
                )
            ).is_presented()
        except Exception as e:
            print(f"android swipe to element exception: {e}")
            return False

    async def _find_element_with_swipe(
        self, selector: Tuple[By, str], scrollable_selector: Tuple[By, str] = None
    ) -> bool:
        if await Element(android_selector=selector, ios_selector=selector).is_presented():
            print("no need to swipe, returning")
            return True
        if self.is_android:
            return await self._swipe_to_element_android(selector, scrollable_selector)
        else:
            return await self._swipe_to_element_ios(selector)

    async def _wait_for_page_to_be_loaded(self, element: Element, timeout: Optional[int] = None):
        try:
            await element.wait_for_presence(timeout)
        except AppiumError as e:
            raise e.__class__(f"{self.__class__.__name__} is not loaded. Error is: {e.message}", e.stacktrace) from e

    async def wait_for_page_to_be_loaded(self, timeout: Optional[int] = None):
        if not self.unique_element:
            raise RuntimeError(
                f"Unique element to check whether the page was loaded "
                f"is not specified in class {self.__class__.__name__}"
            )
        await self._wait_for_page_to_be_loaded(self.unique_element, timeout)

    async def swipe_left(self):
        window_size = await self.session.get_window_rect()
        x = int(window_size.width * 0.85)
        y = int(window_size.height / 2)

        actions = (
            ActionsBuilder()
            .init_touch_actions()
            .mouse_move(x, y, 250)
            .pointer_down(0)
            .pause(200)
            .mouse_move(10, y, 250)
            .pointer_up(0)
            .build()
        )
        await self.session.execute_actions_chain(actions)

    async def check_elements_presence(self, *args: Element):
        result = await asyncio.gather(
            *[element.wait_for_presence_on_screen(screen_name=self.__class__.__name__) for element in args],
            return_exceptions=True,
        )
        errors = [item for item in result if isinstance(item, Exception)]
        if errors:
            raise BaseExceptionGroup("Check all elements execptions:", errors)
