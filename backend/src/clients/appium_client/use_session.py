from src.clients.appium_client.base_test import mobile_test_context
from src.clients.appium_client.session import Session


class UseSessionMixin:
    @property
    def session(self) -> Session:
        context = mobile_test_context.get()
        if not context or not context.session:
            raise RuntimeError("Mobile tests can only run in mobile test context. Inherit Base Mobile Test.")
        return context.session
