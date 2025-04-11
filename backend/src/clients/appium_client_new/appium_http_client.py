import uuid
from typing import Callable, Dict

from pydantic import BaseModel
from yarl import URL

from src.clients.appium_client_new.errors import check_response_error
from src.clients.http_client.reach_client import ReachHttpClient
from src.utils.rate_limiter import RateLimiter


class AppiumClientRateLimiter(RateLimiter):
    pass


class AppiumHttpClient(ReachHttpClient):
    def __init__(self, session_exception_callback: Callable):
        super().__init__(
            name="Appium Server Client",
            base_url=URL("http://host.docker.internal:4723/"),
            limit=AppiumClientRateLimiter(100),
        )
        self.error_callback = session_exception_callback

    @property
    def connection_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive",
            "X-Idempotency-Key": str(uuid.uuid4()),
        }

    async def get(
        self,
        uri: str,
        params: BaseModel | Dict | None = None,
        **kwargs,
    ) -> Dict:
        params = params.model_dump(exclude_none=True, by_alias=True) if isinstance(params, BaseModel) else params
        response = await super().get(uri, params=params, **kwargs)
        await check_response_error(response=response, session_exception_callback=self.error_callback)
        return response.data

    async def post(
        self,
        uri: str,
        json: BaseModel | Dict | None = None,
        **kwargs,
    ) -> Dict:
        json = json.model_dump(exclude_none=True, by_alias=True) if isinstance(json, BaseModel) else json
        response = await super().post(uri, json=json, headers=self.connection_headers, **kwargs)
        await check_response_error(response=response, session_exception_callback=self.error_callback)
        return response.data

    async def delete(self, uri: str, **kwargs) -> Dict:
        response = await super().delete(uri, headers=self.connection_headers, **kwargs)
        await check_response_error(response=response, session_exception_callback=None)
        return response.data
