from typing import List, Self

from arsenic.constants import SelectorType
from arsenic.session import Element


class WebElement(Element):
    async def get_element(self, selector: str, selector_type=SelectorType.xpath) -> Self:
        return await super().get_element(selector, selector_type)

    async def get_elements(self, selector: str, selector_type=SelectorType.xpath) -> List[Self]:
        return await super().get_elements(selector, selector_type)


class WebSelector:
    def __init__(self, selector: str, selector_type: SelectorType = SelectorType.xpath):
        self.selector = selector
        self.selector_type = selector_type
