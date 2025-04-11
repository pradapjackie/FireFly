from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ROOT_PATH: Path = Path("src/modules/load_test_runner/load_tests")


settings = Settings()
