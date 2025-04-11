from contextvars import ContextVar

from pydantic import BaseModel, ConfigDict
from yarl import URL

from src.clients.appium_client.schemas import DesiredCapabilities
from src.clients.appium_client.session import Session
from src.modules.auto_test.test_abs import TestAbs
from src.modules.auto_test.utils.add_auto_test_warinig import add_warning_to_test
from src.modules.auto_test.utils.assets_helper import AssetsHelper
from src.modules.environment.env import env
from src.utils.dynamic_form import MobilePlatformEnum, StringField, AppiumCapabilitiesValue


class MobileTestContext(BaseModel):
    os: MobilePlatformEnum
    session: Session | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


mobile_test_context: ContextVar[MobileTestContext] = ContextVar("mobile_test_context")


class BaseMobileTest(TestAbs):
    class RunConfig:
        ip_address = StringField(label="Emulator IP address")

    assets_helper: AssetsHelper | None = None

    def __init__(self, browserstack_options: AppiumCapabilitiesValue):
        self.session: Session | None = None
        self._session_id = None
        self.auto_accept_alert = True
        self.browserstack_options = browserstack_options

    @classmethod
    async def group_setup(cls):
        cls.assets_helper = AssetsHelper()

    async def setup(self, **test_params):
        desired_capabilities = DesiredCapabilities(
            auto_accept_alerts=self.auto_accept_alert,
            auto_grant_permissions=True,
            device_name=self.browserstack_options.device,
            platform_name=self.browserstack_options.os.capitalize(),
            platform_version=self.browserstack_options.version,
            app=self.browserstack_options.app,
            device_orientation="portrait",
            unicode_keyboard=True,
            reset_keyboard=True,
            new_command_timeout=180,
            language="en",
            locale="US",
            project="Firefly mobile auto",
            build=f"Automation for {self.browserstack_options.os}",
            network_logs=True,
            app_wait_activity=env.appium_app_wait_activity,
            app_package=env.appium_app_package,
        )
        self.session = Session(URL(env.appium_url), "user", "password")
        await self.session.start(desired_capabilities)
        mobile_test_context.set(MobileTestContext(os=self.browserstack_options.os, session=self.session))

    async def teardown(self, **test_params):
        screenshot_in_bytes = None
        if self.session and self.session.started:
            screenshot_in_bytes = await self.session.get_screenshot()
            self._session_id = self.session.id
            await self.session.stop()

        if screenshot_in_bytes:
            try:
                await self.assets_helper.add_image("Screenshot on completion", screenshot_in_bytes)
            except Exception as e:
                add_warning_to_test(f"Exception on screenshot upload to FTP: {e}")

    @classmethod
    async def group_teardown(cls):
        cls.assets_helper and await cls.assets_helper.close_connection()

    @property
    def is_android(self) -> bool:
        return mobile_test_context.get().os == MobilePlatformEnum.android

    @property
    def is_ios(self) -> bool:
        return mobile_test_context.get().os == MobilePlatformEnum.ios
