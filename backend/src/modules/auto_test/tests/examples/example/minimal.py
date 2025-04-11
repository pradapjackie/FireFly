from src.modules.auto_test.register import params, register
from src.modules.auto_test.test_abs import TestAbs


@register()  # Only classes with this decorator are considered as test classes.
class Minimal(TestAbs):  # All test classes must inherit from the TestAbs class. Multiple inheritance allowed.
    # All test methods must have this decorator in order to correctly display iterations on UI.
    @params(
        [
            # The iteration name is required. This name will be displayed on UI and will not be passed to the autotest.
            dict(iteration_name="First"),
        ]
    )
    # The test method name must begin or end with the word test. This is necessary only for the purity of the code.
    async def test_success(self):
        pass
