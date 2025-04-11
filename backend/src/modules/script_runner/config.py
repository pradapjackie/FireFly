from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ROOT_PATH: Path = Path("src/modules/script_runner/scripts")


settings = Settings()
