from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from src.utils.pydantic_helper import CamelCaseModel, all_optional

from ..utils import AppiumCapabilitiesModel


class DesiredCapabilities(AppiumCapabilitiesModel):
    auto_accept_alerts: bool
    auto_grant_permissions: bool
    device_name: str
    platform_name: str
    platform_version: str
    app: str
    device_orientation: str
    unicode_keyboard: bool
    reset_keyboard: bool
    new_command_timeout: int
    language: str
    locale: str
    project: str
    build: str
    enable_multi_windows: bool = True
    network_logs: bool = Field(alias="appium:browserstack.networkLogs")
    browserstack_local: bool = Field(alias="appium:browserstack.local")
    browserstack_local_identifier: str = Field(alias="appium:browserstack.localIdentifier")
    app_wait_activity: Optional[str] = None
    app_package: Optional[str] = None


class Capabilities(CamelCaseModel):
    first_match: List[Dict] = [{}]  # https://www.w3.org/TR/webdriver/#processing-capabilities
    always_match: DesiredCapabilities


class CreateSessionRequest(CamelCaseModel):
    capabilities: Capabilities


class BrowserStackLocalOptions(CamelCaseModel):
    local_identifier: str
    appium_version: str


@all_optional
class NewSessionCapabilities(CamelCaseModel):
    web_storage_enabled: bool
    location_context_enabled: bool
    browser_name: str
    platform: str
    javascript_enabled: bool
    database_enabled: bool
    takes_screenshot: bool
    network_connection_enabled: bool
    platform_name: str
    browser_stack_local_options: BrowserStackLocalOptions = Field(alias="bstack:options")
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
    browserstack_is_target_based: bool = Field(alias="browserstack.isTargetBased")
    auto_accept_alerts: bool
    auto_grant_permissions: bool
    unicode_keyboard: bool
    reset_keyboard: bool
    language: str
    locale: str
    project: str
    build: str
    enable_multi_windows: bool
    network_logs: bool = Field(alias="browserstack.networkLogs")
    browserstack_local: bool = Field(alias="browserstack.local")
    browserstack_local_identifier: str = Field(alias="browserstack.localIdentifier")
    udid: str
    webkit_response_timeout: int
    safari_initial_url: str
    wait_for_quiescence: bool
    wda_startup_retries: int
    bundle_id: str
    app_package: str


class Session(CamelCaseModel):
    capabilities: NewSessionCapabilities
    session_id: str


@all_optional
class StopSessionResponse(BaseModel):
    state: str
    status: int
    value: str | None = None


class WindowRect(BaseModel):
    width: int
    height: int
    x: int
    y: int


@all_optional
class TerminateAppBody(CamelCaseModel):
    bundle_id: str
    app_id: str
