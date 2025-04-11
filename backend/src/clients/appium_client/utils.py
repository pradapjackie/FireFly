from pydantic import BaseModel, ConfigDict

from src.utils.format import snake_to_camel

APPIUM_PREFIX = "appium"
W3C_CAPABILITY_NAMES = frozenset(
    [
        "acceptInsecureCerts",
        "browserName",
        "browserVersion",
        "platformName",
        "pageLoadStrategy",
        "proxy",
        "setWindowRect",
        "timeouts",
        "unhandledPromptBehavior",
    ]
)


def alias_generator(string: str) -> str:
    name = snake_to_camel(string)
    return name if name in W3C_CAPABILITY_NAMES or ":" in name else f"{APPIUM_PREFIX}:{name}"


class AppiumCapabilitiesModel(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generator, populate_by_name=True)
