from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from src.modules.auto_test.register import params, register
from src.modules.auto_test.step_manager import step
from src.modules.auto_test.test_abs import TestAbs
from src.modules.auto_test.utils.add_auto_test_warinig import add_warning_to_test
from src.modules.auto_test.utils.assets_helper import AssetsHelper
from src.modules.environment.env import env
from src.utils.compare_pydantic_models import compare_pydantic_models
from src.utils.dynamic_form import AutocompleteFiled, CheckboxFiled, NumberField, StringField, SwitchFiled
from src.utils.random_info import add_info_to_test_generated_params, random_string


class TestEnum(StrEnum):
    a = "a"
    b = "b"


class ExampleInnerResponse(BaseModel):
    inner_status: str


class ExampleResponse(BaseModel):
    status: str
    data: List[str]
    inner: ExampleInnerResponse


class FirstParentClass(TestAbs):
    # This method is executed once! for all tests in the class.
    # This breaks isolation so use this method only for performance reasons where it is safe to do so.
    # For example, creating TCP connections, connecting to auxiliary services, etc.
    @classmethod
    async def group_setup(cls):
        print("Group setup")

    # This method is executed once before each test iteration.
    async def setup(self, **test_params):
        print("First parent setup")

    # This method is executed once after each test iteration.
    async def teardown(self, **test_params):
        print("First parent teardown")

    # This method is executed once! for all tests in the class.
    # Use it to clean up resources created at group setup
    @classmethod
    async def group_teardown(cls):
        print("Group teardown")


# You can use any inheritance depth.
# All group_setup, setup, group_teardown and teardown methods of both the test class itself and the parents
# will be executed in reverse mro order.
class SecondParentClass(FirstParentClass):
    async def setup(self, **test_params):
        print("Second parent setup")

    async def teardown(self, **test_params):
        print("Second parent teardown")


@register()
class Maximum(SecondParentClass):
    # Sometimes tests need to save test, pictures, or video. Use this class for that.
    assets_helper: Optional[AssetsHelper] = None

    @classmethod
    async def group_setup(cls):
        # One instance of this class can be used for different tests, this will not break their isolation.
        # Therefore, this is a good example of what can be used in group setup
        cls.assets_helper = AssetsHelper()

    @classmethod
    async def group_teardown(cls):
        # Don't forget to clean resources.
        cls.assets_helper and await cls.assets_helper.close_connection()

    # Sometimes, for various reasons, tests require additional configuration beyond the environment.
    # You can add any required configuration using this inner class.
    class RunConfig:
        string_field = StringField(label="Some String", placeholder="string...")
        number_field = NumberField(label="Some Number", placeholder="number...")
        checkbox_field = CheckboxFiled(label="Some Checkbox", placeholder="check me")
        autocomplete_field = AutocompleteFiled(
            label="Some Autocomplete", placeholder="choose me", options=["First", "Second", "Third"]
        )
        switch_field = SwitchFiled(label="Some Switch", placeholder="switch me")

    @params(
        [
            #  All parameters must be json serializable
            dict(
                iteration_name="Success",
                fail=False,
                status="success",
                int_param=10,
                array_param=["a", "c"],
                enum_param=TestEnum.a,
            ),
            dict(
                iteration_name="Fail",
                fail=True,
                status="success",
                int_param=20,
                array_param=["aa", "cc"],
                enum_param=TestEnum.b,
            ),
            dict(
                iteration_name="Fail by compare",
                fail=False,
                status="fail",
                int_param=20,
                array_param=["aa", "cc"],
                enum_param=TestEnum.b,
            ),
        ]
    )
    async def test_success(self, fail: bool, status: str, int_param: int, array_param: List[str], enum_param: TestEnum):
        # Add a description to your tests - it will be reflected in the UI.
        """
        My Test description
        """

        # Always use steps to improve the structure of the code and display them on the UI
        async with step("Start"):
            # Nesting can be any
            async with step("Continue"):
                pass

        async with step("Print test params"):
            print(int_param)
            print(array_param)
            print(enum_param)
        async with step("Print test run config"):
            print(self.RunConfig.number_field.value)
            print(self.RunConfig.string_field.value)
            print(self.RunConfig.checkbox_field.value)
            print(self.RunConfig.autocomplete_field.value)
            print(self.RunConfig.switch_field.value)

        async with step("Print env variable"):
            # Certain values may differ from environment to environment: application and database URLs, passwords, ...
            # Such variables need to be stored in the environment. They can be easily changed through the UI
            print(env.test_env_variable)

        async with step("Add generated param"):
            # Tests generate both random (for example, name of a new client) and new (for example, new client id) data.
            # Use this method to display them on the UI for easier analysis and debugging.
            add_info_to_test_generated_params("Random string", random_string(10))

        async with step("Add asset"):
            # Adding a text document to FTP. This can be, for example, logs,
            # or using other methods, you can save a screenshot or video.
            await self.assets_helper.add_text("Some text", b"Some text")

        async with step("Add warning"):
            add_warning_to_test("Test Warning")

        # await asyncio.sleep(300)

        async with step("Check error"):
            if fail:
                # Any exception will terminate the test and correctly display the error on UI.
                # Of course, clean up steps (teardown, group teardown) will be executed.
                raise RuntimeError("Runtime error")

        async with step("Compare some data"):
            real_result = ExampleResponse(
                status="success", data=["a", "b"], inner=ExampleInnerResponse(inner_status=status)
            )
            expected_result = ExampleResponse(
                status="success", data=["a", "b"], inner=ExampleInnerResponse(inner_status="success")
            )
            # To validate API responses, database events and more, use the following method
            compare_pydantic_models(real=real_result, expected=expected_result)
