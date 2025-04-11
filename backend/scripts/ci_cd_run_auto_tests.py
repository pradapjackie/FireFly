import asyncio
import json
from enum import StrEnum
from typing import Optional, Tuple

import aiohttp
import click
import websockets
from aiohttp import TCPConnector

# Global
FIREFLY_SYNC = "https://FIREFLY_PUBLIC_HOST"
FIREFLY_ASYNC = "wss://FIREFLY_PUBLIC_HOST"
TOKEN = "FIREFLY_CI_CD_TOKEN"


class EnvEnum(StrEnum):
    trunk = "trunk"
    staging = "staging"
    prod = "prod"


class RunScript:
    def __init__(self, tags: Tuple[str], env: EnvEnum, root_folder: str):
        self.tags = tags
        self.env_name = env
        self.root_folder = root_folder

        self.test_run_id: Optional[str] = None

    async def start_test_run(self):
        payload = {
            "root_folder": self.root_folder,
            "env_name": self.env_name,
            "tags": self.tags,
            "test_ids": [],
            "setting_overwrite": {},
            "run_config": {},
        }
        try:
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.post(
                    f"{FIREFLY_SYNC}/api/autotest/run/", json=payload, headers={"Authorization": f"Bearer {TOKEN}"}
                ) as resp:
                    assert resp.status == 200, f"The test did not start. Error: {resp.status} {await resp.read()}"
                    response = await resp.json()
                    self.test_run_id = response["id"]
        except Exception as e:
            raise RuntimeError(f"Exception on autotests startup: {e}") from e

    async def wait_for_complete(self):
        try:
            async with asyncio.timeout(60 * 120):
                async with websockets.connect(
                    f"{FIREFLY_ASYNC}/api/autotest/ws/test_run/{self.test_run_id}"
                ) as websocket:
                    async for message in websocket:
                        message = json.loads(message)
                        if message["channel"] == "test_run" and message["data"]["status"] == "success":
                            break
        except Exception as e:
            raise RuntimeError(f"Error while waiting for test run results: {e}") from e

    def get_result_link(self) -> str:
        return f"{FIREFLY_SYNC}/auto/history/{self.root_folder}/{self.test_run_id}"


async def main(**kwargs):
    runner = RunScript(**kwargs)
    await runner.start_test_run()
    await runner.wait_for_complete()
    print(runner.get_result_link())


@click.command()
@click.option("--tags", type=click.STRING, multiple=True)
@click.option("--env", type=click.Choice(list(EnvEnum)), default=EnvEnum.trunk)
@click.option("--brand", type=click.STRING)
def main_sync(tags: Tuple[str], env: EnvEnum, root_folder: str):
    asyncio.run(main(tags=tags, env=env, brand=root_folder))


if __name__ == "__main__":
    main_sync()
