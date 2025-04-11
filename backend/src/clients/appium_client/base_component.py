from typing import Optional, Tuple

from src.clients.appium_client import schemas
from src.clients.appium_client.base_test import mobile_test_context
from src.clients.appium_client.element import DynamicElement
from src.clients.appium_client.unified_selector import UnifiedSelector


class BaseComponent:
    @property
    def is_android(self) -> bool:
        return mobile_test_context.get().os == schemas.MobilePlatformEnum.android

    @property
    def is_ios(self) -> bool:
        return mobile_test_context.get().os == schemas.MobilePlatformEnum.ios


class ComponentWithLocator(BaseComponent):
    def __init__(
        self,
        android_selector: Optional[Tuple[schemas.By, str]] = None,
        ios_selector: Optional[Tuple[schemas.By, str]] = None,
    ):
        self._locator = UnifiedSelector(android_selector=android_selector, ios_selector=ios_selector)
        self._element = DynamicElement(android_selector=android_selector, ios_selector=ios_selector)

    async def is_presented(self) -> bool:
        return await self._element.is_presented()

    def set_dynamic_attrs(self, **kwargs):
        self._element.set_dynamic_attrs(**kwargs)

    @property
    def current_selector(self) -> UnifiedSelector:
        return self._element.current_selector
