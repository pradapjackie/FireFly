from typing import Any, Dict, List, Optional

from aiochclient import ChClient
from aiohttp import ClientSession, TCPConnector


class ClickHouseClient(ChClient):
    def __init__(
        self, host: str, port: int, user: str, password: str, database: str, compress_response: bool = False, **settings
    ):
        # noinspection HttpUrlsUsage
        super().__init__(
            session=ClientSession(connector=TCPConnector(ssl=False)),
            url=f"http://{host}:{port}/",
            user=user,
            password=password,
            database=database,
            compress_response=compress_response,
            **settings,
        )

    async def fetch(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> List[Dict]:
        result = await super().fetch(query, *args, json=json, params=params, query_id=query_id, decode=decode)
        return [dict(zip(item.keys(), item.values())) for item in result]
