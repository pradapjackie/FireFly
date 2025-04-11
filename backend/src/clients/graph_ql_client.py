from pathlib import Path

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

from src.modules.auto_test.step_manager import step
from src.utils.jwt_gen import generate_jwt_token


class GraphQlClient:
    def __init__(self, url: str, key_path: Path):
        self.url = url
        self.key_path = key_path

    async def execute(self, query: str, client_id: str, query_name: str):
        async with step(f"Execute {query_name} GraphQL request"):
            headers = {"Authorization": f"Bearer {generate_jwt_token(self.key_path, client_id)}"}
            transport = AIOHTTPTransport(url=self.url, headers=headers)
            async with Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=50) as session:
                return await session.execute(gql(query))

    async def subscribe(self, query: str, client_id: str, name: str):
        async with step(f"Execute GraphQL subscription: {name}"):
            headers = {"authToken": generate_jwt_token(self.key_path, client_id)}
            transport = WebsocketsTransport(url=self.url.replace("http", "ws", 1), init_payload=headers)

            async with Client(transport=transport, execute_timeout=1) as client:
                async for resp in client.subscribe(gql(query)):
                    yield resp
