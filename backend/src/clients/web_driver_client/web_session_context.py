from contextvars import ContextVar

from src.clients.web_driver_client.schemas import WebSessionContext

web_session_context: ContextVar[WebSessionContext] = ContextVar("web_session_context")
