import asyncio

from fastapi import WebSocket, WebSocketDisconnect

from src.cache.base import RedisChannel
from src.schemas.common import SubscribeMessage, SuccessfulSubscribeMessage


class EventManager:
    def __init__(self, channel: RedisChannel):
        self.channel = channel
        self.execution_id: str | None = None
        self.proxy_task: asyncio.Task | None = None

    async def listen_with_subscription(self, websocket: WebSocket):
        try:
            while True:
                message = await websocket.receive_text()
                message = SubscribeMessage.model_validate_json(message)
                if message.execution_id is None:
                    self.proxy_task and self.proxy_task.cancel()
                if self.execution_id != message.execution_id:
                    self.proxy_task and self.proxy_task.cancel()
                    self.proxy_task = asyncio.create_task(self.channel.proxy_to_ws(message.execution_id, websocket))
                    await websocket.send_text(
                        SuccessfulSubscribeMessage(
                            load_test_id=message.load_test_id, execution_id=message.execution_id
                        ).model_dump_json()
                    )
        except WebSocketDisconnect:
            self.proxy_task and self.proxy_task.cancel()
