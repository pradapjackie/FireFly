from ssl import SSLContext
from typing import AsyncIterator, Dict, List, Tuple, Type, TypeVar

from aiokafka import AIOKafkaConsumer

from src.utils.pydantic_helper import BaseResponse

KafkaMessageResponseModel = TypeVar("KafkaMessageResponseModel", bound=BaseResponse)


class KafkaClient:
    def __init__(
        self,
        *topics,
        servers: List[str],
        ssl_context: SSLContext,
        consumer_group: str,
        user_name: str,
        password: str,
        message_models: Dict[str, Type[KafkaMessageResponseModel]],
    ):
        self.topics = topics
        self.servers = servers
        self.ssl_context = ssl_context
        self.consumer_group = consumer_group
        self.user_name = user_name
        self.password = password
        self.message_models = message_models
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=servers,
            security_protocol="SASL_SSL",
            ssl_context=ssl_context,
            group_id=consumer_group,
            sasl_mechanism="PLAIN",
            sasl_plain_username=user_name,
            sasl_plain_password=password,
        )

    async def read(self) -> AsyncIterator[Tuple[int, KafkaMessageResponseModel]]:
        try:
            await self.consumer.start()
            async for msg in self.consumer:
                yield msg.offset, self.message_models[msg.topic].model_validate_json(msg.value.decode("UTF-8"))
        finally:
            await self.consumer.stop()
