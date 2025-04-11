import asyncio
from dataclasses import dataclass
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, Optional

import httpx
from aiohttp.typedefs import StrOrURL
from multidict import CIMultiDictProxy
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from zeep import AsyncClient
from zeep.exceptions import TransportError
from zeep.helpers import serialize_object
from zeep.transports import AsyncTransport

from src.clients.http_client.client import HttpClient


@dataclass
class SoapHttpResponse:
    status_code: int
    text: str
    raw: bytes
    headers: CIMultiDictProxy[str]
    cookies: SimpleCookie[str]
    encoding: str

    def read(self):
        return self.raw


class SoapHttpClient(HttpClient):
    async def post(self, address: StrOrURL, content: Any, headers: Any) -> SoapHttpResponse:
        async with self.http_session.post(url=address, data=content, headers=headers) as resp:
            return SoapHttpResponse(
                status_code=resp.status,
                text=await resp.text(),
                raw=await resp.read(),
                headers=resp.headers,
                cookies=resp.cookies,
                encoding=resp.get_encoding(),
            )


class SoapHttpSyncClient(httpx.Client):
    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        if args[0] == "http://schemas.xmlsoap.org/soap/encoding/":
            filepath = Path(__file__).parent / "soap_encoding.xml"
            with open(filepath, mode="rb") as f:
                result._content = f.read()
                result.status_code = 200
        return result


class SoapClient:
    def __init__(self, wsdl_url: str, ns_headers: Optional[dict] = None):
        self.wsdl_url = wsdl_url
        self.ns_headers = ns_headers
        self._http_client = SoapHttpClient()
        self._sync_http_client = SoapHttpSyncClient(follow_redirects=True, timeout=httpx.Timeout(30))
        self._soap_client: Optional[AsyncClient] = None

    @staticmethod
    @retry(
        retry=retry_if_exception_type(TransportError),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        reraise=True,
    )
    def _create_soap_client(url, transport):
        return AsyncClient(url, transport=transport)

    async def _get_soap_client(self):
        if not self._soap_client:
            transport = AsyncTransport(client=self._http_client, wsdl_client=self._sync_http_client)
            self._soap_client = await asyncio.get_event_loop().run_in_executor(
                None, self._create_soap_client, self.wsdl_url, transport
            )
            if self.ns_headers:
                for prefix, header in self.ns_headers.items():
                    self._soap_client.set_ns_prefix(prefix, header)
        return self._soap_client

    async def call(self, method: str, params: BaseModel):
        client = await self._get_soap_client()
        result = await getattr(client.service, method)(**params.model_dump(by_alias=True))
        return serialize_object(result, dict)

    async def close(self) -> None:
        self._soap_client = None
        await self._http_client.close()
        self._sync_http_client.close()
