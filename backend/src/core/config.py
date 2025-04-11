import pathlib
import secrets
from typing import Any, Optional

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    ALGORITHM: str = "HS256"

    CELERY_BROKER: str
    CELERY_BACKEND: str

    REDIS_CACHE: str

    DB_SERVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    FIRST_USER_EMAIL: str
    FIRST_USER_FULLNAME: str
    FIRST_USER_PASSWORD: str

    SQLALCHEMY_SYNC_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_ASYNC_DATABASE_URI: Optional[str] = None

    RUN_TEST_IN_MAIN_LOOP: bool = False

    MINIO_HOST: str
    MINIO_PUBLIC_HOST: str | None = None
    MINIO_BUCKET_NAME: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str

    @field_validator("SQLALCHEMY_SYNC_DATABASE_URI", mode="before")
    def assemble_sync_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return (
            f"mysql+pymysql://"
            f'{info.data.get("DB_USER")}:{info.data.get("DB_PASSWORD")}@'
            f'{info.data.get("DB_SERVER")}/{info.data.get("DB_NAME")}'
        )

    @field_validator("SQLALCHEMY_ASYNC_DATABASE_URI", mode="before")
    def assemble_async_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return (
            f"mysql+asyncmy://"
            f'{info.data.get("DB_USER")}:{info.data.get("DB_PASSWORD")}@'
            f'{info.data.get("DB_SERVER")}/{info.data.get("DB_NAME")}'
        )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=pathlib.Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
