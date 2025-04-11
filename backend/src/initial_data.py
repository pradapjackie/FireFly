import asyncio
import logging

from db.init_db import create_initial_data_in_db, run_migrations, wait_for_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    await wait_for_db()
    await run_migrations()
    await create_initial_data_in_db()


def main() -> None:
    logger.info("Start DB initialization")
    asyncio.get_event_loop().run_until_complete(init())
    logger.info("DB initialization completed")


if __name__ == "__main__":
    main()
