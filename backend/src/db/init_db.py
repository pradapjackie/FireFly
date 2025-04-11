import logging

from sqlalchemy import text
from tenacity import retry, stop_after_attempt, wait_fixed

from alembic import command
from alembic.config import Config
from src import crud, schemas
from src.core.config import settings
from src.db import base  # noqa: F401
from src.db.session import SessionLocal, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
async def wait_for_db():
    logger.info("Checking database availability...")
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("Database is available")


async def run_migrations():
    logger.info("Starting database migration...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Database migration completed")


async def create_initial_data_in_db() -> None:
    logger.info("Starting database migration...")
    async with SessionLocal() as db:
        user = await crud.user.get_by_email(db, email=settings.FIRST_USER_EMAIL)
        if not user:
            user_in = schemas.UserCreate(
                email=settings.FIRST_USER_EMAIL,
                password=settings.FIRST_USER_PASSWORD,
                full_name=settings.FIRST_USER_FULLNAME,
            )
            await crud.user.create(db, obj_in=user_in)
            logger.info("Initial data created")
        else:
            logger.info("Initial data has already been created")
