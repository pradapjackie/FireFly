from typing import Any, Callable, Dict, Type, Union

from src.clients.http_client.reach_client import BaseHttpResponse

STATUS_SUCCESS = 0


class BaseAppiumError(Exception):
    pass


class AppiumError(BaseAppiumError):
    def __init__(self, message, stacktrace):
        self.message = message
        self.stacktrace = stacktrace
        super().__init__(message)


class UnknownAppiumError(BaseAppiumError):
    pass


class SessionInterruptedError(AppiumError):
    pass


CODES: Dict[Union[str, int], Type[AppiumError]] = {}


def get(error_code: Union[str, int]) -> Type[AppiumError]:
    return CODES.get(error_code, UnknownAppiumError)


def create(error_name: str, *error_codes: int) -> Type[AppiumError]:
    name = "".join(bit.capitalize() for bit in error_name.split(" "))
    # noinspection PyTypeChecker
    cls: Type[AppiumError] = type(name, (AppiumError,), {})
    CODES[error_name] = cls
    for code in error_codes:
        CODES[code] = cls
    return cls


# Keep in sync with org.openqa.selenium.remote.ErrorCodes
# https://www.programcreek.com/java-api-examples/?code=SeleniumHQ/selenium/selenium-master/java/client/src/org/openqa/selenium/remote/ErrorCodes.java#
NoSuchElement = create("no such element", 7)
NoSuchFrame = create("no such frame", 8)
UnknownCommand = create("unknown command", 9)
StaleElementReference = create("stale element reference", 10)
ElementNotVisible = create("element not visible", 11)
InvalidElementState = create("invalid element state", 12)
UnknownError = create("unknown error", 13)
ElementNotInteractable = create("element not interactable")
ElementIsNotSelectable = create("element is not selectable", 15)
JavascriptError = create("javascript error", 17)
Timeout = create("timeout", 21)
NoSuchWindow = create("no such window", 23)
InvalidCookieDomain = create("invalid cookie domain", 24)
UnableToSetCookie = create("unable to set cookie", 25)
UnexpectedAlertOpen = create("unexpected alert open", 26)
NoSuchAlert = create("no such alert", 27)
ScriptTimeout = create("script timeout", 28)
InvalidElementCoordinates = create("invalid element coordinates", 29)
IMENotAvailable = create("ime not available", 30)
IMEEngineActivationFailed = create("ime engine activation failed", 31)
InvalidSelector = create("invalid selector", 32)
MoveTargetOutOfBounds = create("move target out of bounds", 34)

# exceptions that may indicate errors within appium client
ERROR_CLASSES = (UnknownAppiumError, UnknownCommand, UnknownError)


async def raise_exception(data: Dict[str, Any], session_exception_callback: Callable | None = None):
    error = data.get("status") or data.get("error") or data.get("state")

    if "value" in data and isinstance(data["value"], dict):
        data = data["value"]

    if error is None and "error" in data:
        error = data["error"]

    message = data.get("message")
    stacktrace = data.get("stacktrace")

    if message == "Session not started or terminated":
        exception_class = SessionInterruptedError
        session_exception_callback and await session_exception_callback()
    else:
        exception_class = get(error)
    raise exception_class(message, stacktrace)


async def check_response_error(response: BaseHttpResponse, session_exception_callback: Callable | None = None) -> None:
    data = response.data
    if response.status_code >= 400:
        await raise_exception(data, session_exception_callback)
    if not isinstance(data, dict) or data.get("status") is None or data.get("status") == STATUS_SUCCESS:
        return
    await raise_exception(data, session_exception_callback)
