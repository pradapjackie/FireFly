from typing import Optional, Tuple

from src.clients.appium_client.base_test import mobile_test_context
from src.clients.appium_client.schemas import MobilePlatformEnum


class UnifiedSelector(tuple):
    def __new__(
        cls, android_selector: Optional[Tuple[str, str]] = None, ios_selector: Optional[Tuple[str, str]] = None
    ):
        os = mobile_test_context.get().os
        if os == MobilePlatformEnum.android and android_selector:
            return tuple.__new__(UnifiedSelector, android_selector)
        elif os == MobilePlatformEnum.ios and ios_selector:
            return tuple.__new__(UnifiedSelector, ios_selector)
        else:
            return tuple.__new__(UnifiedSelector, (None,))

    def get_dynamic_selector(self, **kwargs) -> Tuple[str, str]:
        return self[0], self[1].format(**kwargs)

    def __getitem__(self, item) -> str:
        if len(self) == 1:
            raise RuntimeError(f"UnifiedSelector for {mobile_test_context.get().os} is not specified")
        return super().__getitem__(item)
