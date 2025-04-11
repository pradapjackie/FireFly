from contextlib import asynccontextmanager
from types import ModuleType
from typing import Callable, Optional, Self, Type, TypeVar

from grpc import ChannelConnectivity, StatusCode, aio
from pydantic import BaseModel

from src.modules.auto_test.step_manager import step
from src.utils.pydantic_helper import FromProtobufModel
from src.utils.rate_limiter import RateLimiter

GrpcResponseModel = TypeVar("GrpcResponseModel", bound=FromProtobufModel)


class RpcException(Exception):
    def __init__(self, e: aio.AioRpcError, host: str, stub_name: str, method_name: str, request: BaseModel):
        self.code = e.code()
        self.message = f"""
            RPC error :
                status = {e.code()}
                details = "{e.details()}"
                debug_error_string = "{e.debug_error_string()}"
            On server {host}. Stub: {stub_name}
            On method {method_name} with request data:
            {request.model_dump_json()}
            """
        super().__init__(self.message)


class RpcNotFoundException(RpcException):
    def __init__(self, e: aio.AioRpcError, host: str, stub_name: str, method_name: str, request: BaseModel):
        super().__init__(e, host, stub_name, method_name, request)


class GrpcClient:
    def __init__(self, host: str, server_stub: Callable, client_pb2: ModuleType, limit: Optional[RateLimiter] = None):
        self.host = host
        self.server_stub = server_stub
        self.client_pb2 = client_pb2
        self._channel: Optional[aio.Channel] = None
        self.limit = limit or RateLimiter(5000)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @asynccontextmanager
    async def get_channel(self):
        async with self.limit:
            if not self._channel:
                self._channel = aio.insecure_channel(self.host)
            if self._channel.get_state() in (ChannelConnectivity.TRANSIENT_FAILURE, ChannelConnectivity.SHUTDOWN):
                await self._channel.close()
                self._channel = aio.insecure_channel(self.host)
            yield self._channel

    def _model_to_grpc_request(self, request: BaseModel):
        return getattr(self.client_pb2, request.__class__.__name__)(
            **request.model_dump(by_alias=True, exclude_none=True)
        )

    def _raise_exception(self, e: aio.AioRpcError, method_name: str, request: BaseModel):
        if e.code() == StatusCode.NOT_FOUND:
            raise RpcNotFoundException(e, self.host, self.server_stub.__name__, method_name, request) from e
        else:
            raise RpcException(e, self.host, self.server_stub.__name__, method_name, request) from e

    async def stream(
        self,
        method_name: str,
        request: BaseModel,
        response_model: Type[GrpcResponseModel],
        metadata: Optional[dict] = None,
        timeout: Optional[int] = None,
    ):
        async with self.get_channel() as channel:
            stub = self.server_stub(channel)
            metadata = tuple(metadata.items()) if metadata else None
            stream = getattr(stub, method_name)(
                self._model_to_grpc_request(request), metadata=metadata, timeout=timeout
            )
            try:
                async for resp in stream.__aiter__():
                    yield response_model.model_validate(resp)
            except aio.AioRpcError as e:
                self._raise_exception(e, method_name, request)

    async def request(
        self,
        method_name: str,
        request: BaseModel,
        response_model: Type[GrpcResponseModel],
        timeout: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> GrpcResponseModel:
        async with self.get_channel() as channel:
            async with step(f"Make {method_name} gRPC request"):
                stub = self.server_stub(channel)
                try:
                    result = await getattr(stub, method_name)(
                        self._model_to_grpc_request(request),
                        timeout=timeout,
                        metadata=tuple(metadata.items()) if metadata else None,
                    )
                except aio.AioRpcError as e:
                    self._raise_exception(e, method_name, request)
                else:
                    return response_model.model_validate(result)

    async def close(self):
        self._channel and await self._channel.close()
