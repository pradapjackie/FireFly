from typing import Dict, List, Literal

from pydantic import BaseModel, ConfigDict

from src.utils.format import snake_to_camel
from src.utils.pydantic_helper import CamelCaseModel, all_optional

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
    return name if name in W3C_CAPABILITY_NAMES or ":" in name else f"appium:{name}"


class DesiredCapabilities(BaseModel):
    automation_name: Literal["flutter", "UiAutomator2"] = "UiAutomator2"
    platform_name: Literal["iOS", "Android"]
    platform_version: str
    device_name: str
    app: str
    auto_accept_alerts: bool
    auto_grant_permissions: bool
    device_orientation: Literal["landscape", "portrait"] = "portrait"
    unicode_keyboard: bool = True
    reset_keyboard: bool = True
    new_command_timeout: int = 180
    language: str = "en"
    locale: str = "US"
    app_wait_activity: str | None = None
    app_package: str | None = None

    model_config = ConfigDict(alias_generator=alias_generator, populate_by_name=True)


class Capabilities(CamelCaseModel):
    first_match: List[Dict] = [{}]  # https://www.w3.org/TR/webdriver/#processing-capabilities
    always_match: DesiredCapabilities


@all_optional
class CreatedSessionCapabilities(CamelCaseModel):
    web_storage_enabled: bool
    location_context_enabled: bool
    browser_name: str
    platform: str
    javascript_enabled: bool
    database_enabled: bool
    takes_screenshot: bool
    network_connection_enabled: bool
    platform_name: str
    new_command_timeout: int
    real_mobile: bool
    device_name: str
    safari_ignore_fraud_warning: bool
    orientation: str
    device_orientation: str
    no_reset: bool
    automation_name: str
    use_xctestrun_file: bool
    bootstrap_path: str
    auto_accept_alerts: bool
    auto_grant_permissions: bool
    unicode_keyboard: bool
    reset_keyboard: bool
    language: str
    locale: str
    project: str
    build: str
    enable_multi_windows: bool
    udid: str
    webkit_response_timeout: int
    safari_initial_url: str
    wait_for_quiescence: bool
    wda_startup_retries: int
    bundle_id: str
    app_package: str
