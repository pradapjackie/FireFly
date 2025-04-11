from pathlib import Path
from typing import Pattern, Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TEST_METHOD_PATTERN: Pattern = "(test_.*|.*_test)"
    ROOT_PATH: Path = Path("src/modules/auto_test/tests")
    ITERATION_NAMES: Set[str] = {"iteration_name", "i_name"}
    AUTO_TEST_PENDING_RUNS: str = "pending_test_run_ids"


settings = Settings()
