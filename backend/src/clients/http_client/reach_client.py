from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

import aiohttp
from aiohttp import FormData, MultipartWriter
from pydantic import BaseModel
from yarl import URL

from src.clients.http_client.client import HttpClient
from src.modules.auto_test.step_manager import step
from src.utils.pydantic_helper import BaseResponse
from src.utils.rate_limiter import RateLimiter


class BaseHttpResponse(BaseResponse):
    status_code: int
    data: dict | list | str | bytes | None = None
    headers: Dict[str, str]


class ReachHttpClient(HttpClient):
    def __init__(self, name: str, base_url: URL, limit: RateLimiter, *conn_args, **conn_kwargs):
        super().__init__(*conn_args, **conn_kwargs, connector=aiohttp.TCPConnector(ssl=False))
        self.name = name
        self.base_url = base_url
        self.limit = limit

    @staticmethod
    def check_status_code(url: URL, method: str, status_code: int, expected_status_code: int, **kwargs):
        assert (
            status_code == expected_status_code
        ), f"""
        Request {method.upper()} {url}:
            {"Parameters: " + str(kwargs.get("params")) if kwargs.get("params") else ""} 
            {"Json Body: " + str(kwargs.get("json")) if kwargs.get("json") else ""}
            {"Form Body: " + str(kwargs.get("data")) if kwargs.get("data") else ""}
        Returned an unexpected status code: {status_code}
        Expected Code: {expected_status_code}
        """

    @asynccontextmanager
    async def _call(
        self, uri: str, method: str, expected_status_code: int | None = None, **kwargs
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        uri = uri.lstrip("/") if uri.startswith("/") else uri
        async with step(f"Make {self.name} {method.upper()} request to: {self.base_url / uri}"):
            async with self.limit, getattr(self.http_session, method)(url=self.base_url / uri, **kwargs) as resp:
                expected_status_code and self.check_status_code(
                    url=self.base_url / uri,
                    method=method,
                    status_code=resp.status,
                    expected_status_code=expected_status_code,
                    **kwargs,
                )
                try:
                    yield resp
                except Exception as e:
                    try:
                        resp_data = await resp.read()
                    except Exception as read_error:
                        raise RuntimeError(f"Request decode exception: {resp}; Read error: {read_error}") from e
                    raise RuntimeError(f"Request decode exception: {resp.status} {resp_data}") from e

    @staticmethod
    async def _read_response(resp: aiohttp.ClientResponse, raw: bool = False) -> BaseHttpResponse:
        if raw:
            data = await resp.read()
        else:
            data = await resp.json() if await resp.read() else None
        return BaseHttpResponse(status_code=resp.status, headers=dict(resp.headers), data=data)

    async def get(
        self,
        uri: str,
        raw: bool = False,
        params: BaseModel | Dict | None = None,
        expected_status_code: int | None = None,
        **kwargs,
    ) -> BaseHttpResponse:
        params = params.model_dump(exclude_none=True, by_alias=True) if isinstance(params, BaseModel) else params
        async with self._call(uri, "get", params=params, expected_status_code=expected_status_code, **kwargs) as resp:
            return await self._read_response(resp, raw)

    async def post(
        self,
        uri: str,
        json: BaseModel | Dict | None = None,
        data: BaseModel | FormData | MultipartWriter | Dict | None = None,
        raw: bool = False,
        expected_status_code: int | None = None,
        **kwargs,
    ) -> BaseHttpResponse:
        json = json.model_dump(exclude_none=True, by_alias=True) if isinstance(json, BaseModel) else json
        data = data.model_dump(exclude_none=True, by_alias=True) if isinstance(data, BaseModel) else data
        async with self._call(
            uri, "post", json=json, data=data, expected_status_code=expected_status_code, **kwargs
        ) as resp:
            return await self._read_response(resp, raw)

    async def put(
        self,
        uri: str,
        json: BaseModel | Dict | None = None,
        data: BaseModel | FormData | MultipartWriter | Dict | None = None,
        raw: bool = False,
        expected_status_code: int | None = None,
        **kwargs,
    ) -> BaseHttpResponse:
        json = json.model_dump(exclude_none=True, by_alias=True) if isinstance(json, BaseModel) else json
        data = data.model_dump(exclude_none=True, by_alias=True) if isinstance(data, BaseModel) else data
        async with self._call(
            uri, "put", json=json, data=data, expected_status_code=expected_status_code, **kwargs
        ) as resp:
            return await self._read_response(resp, raw)

    async def patch(
        self,
        uri: str,
        json: BaseModel | Dict | None = None,
        data: BaseModel | FormData | MultipartWriter | Dict | None = None,
        raw: bool = False,
        expected_status_code: int | None = None,
        **kwargs,
    ) -> BaseHttpResponse:
        json = json.model_dump(exclude_none=True, by_alias=True) if isinstance(json, BaseModel) else json
        data = data.model_dump(exclude_none=True, by_alias=True) if isinstance(data, BaseModel) else data
        async with self._call(
            uri, "patch", json=json, data=data, expected_status_code=expected_status_code, **kwargs
        ) as resp:
            return await self._read_response(resp, raw)

    async def delete(
        self, uri: str, raw: bool = False, expected_status_code: int | None = None, **kwargs
    ) -> BaseHttpResponse:
        async with self._call(uri, "delete", expected_status_code=expected_status_code, **kwargs) as resp:
            return await self._read_response(resp, raw)
