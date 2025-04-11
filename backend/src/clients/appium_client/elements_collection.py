from typing import List, Optional, Tuple

from src.clients.appium_client import schemas
from src.clients.appium_client.base_test import mobile_test_context
from src.clients.appium_client.element import BaseElement
from src.clients.appium_client.session import Session
from src.clients.appium_client.unified_selector import UnifiedSelector


class ElementsCollection:
    def __init__(
        self,
        android_selector: Optional[Tuple[schemas.By, str]] = None,
        ios_selector: Optional[Tuple[schemas.By, str]] = None,
    ):
        self.selector = UnifiedSelector(android_selector, ios_selector)
        self.elements: List[BaseElement] = list()

    @property
    def session(self) -> Session:
        context = mobile_test_context.get()
        if not context or not context.session:
            raise RuntimeError("Mobile tests can only run in mobile test context. Inherit Base Mobile Test.")
        return context.session

    async def _find_all(self):
        data = schemas.FindElementRequest(using=self.selector[0], value=self.selector[1])
        elements = await self.session.appium_client.find_elements(self.session.id, data)
        self.elements = list(map(lambda elem: BaseElement(elem.id), elements))

    async def get_elements(self) -> List[BaseElement]:
        if not self.elements:
            await self._find_all()
        return self.elements

    def reset(self):
        self.elements = list()

    async def get_all_texts(self, wait_for_visibility: bool = True) -> List[str]:
        texts = list()
        for el in await self.get_elements():
            if wait_for_visibility:
                await el.wait_for_visibility()
            texts.append(await el.get_text())
        return texts
