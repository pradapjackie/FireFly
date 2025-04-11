from src.clients.appium_client_new.schemas.capabilities import DesiredCapabilities
from src.clients.appium_client_new.session import Session
from src.modules.auto_test.test_abs import TestAbs
from src.modules.auto_test.utils.assets_helper import AssetsHelper
from src.utils.dynamic_form import AutocompleteFiled, StringField


class BaseFlatterMobileTest(TestAbs):
    class RunConfig:
        platform_name = AutocompleteFiled(label="Platform name", options=["Android", "iOS"], default_value="Android")
        platform_version = StringField(label="Platform version", default_value="15.0")
        device_name = StringField(label="Device name", default_value="Pixel 9")
        app_path = StringField(label="App path", default_value="Path\\to\\app-dev-debug.apk")

    assets_helper: AssetsHelper | None = None

    def __init__(self):
        self.session: Session | None = None

    @classmethod
    async def group_setup(cls):
        cls.assets_helper = AssetsHelper()

    async def setup(self, **test_params):
        # noinspection PyTypeChecker
        desired_capabilities = DesiredCapabilities(
            automation_name="flutter",
            platform_name=self.RunConfig.platform_name.value,
            platform_version=self.RunConfig.platform_version.value,
            device_name=self.RunConfig.device_name.value,
            app=self.RunConfig.app_path.value,
            auto_accept_alerts=True,
            auto_grant_permissions=True,
        )
        self.session = await Session().start(desired_capabilities)
        await self.session.wait_for_flutter_first_frame()

    async def teardown(self, **test_params):
        if self.session and self.session.started:
            try:
                screenshot_bytes = await self.session.get_screenshot()
                await self.assets_helper.add_image("Screenshot after completion", screenshot_bytes)
            finally:
                await self.session.stop()

    @classmethod
    async def group_teardown(cls):
        cls.assets_helper and await cls.assets_helper.close_connection()
