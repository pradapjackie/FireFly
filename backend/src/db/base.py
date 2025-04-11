# Import all the models, so that Base has them before being imported by Alembic
from src.db.base_class import Base  # noqa
from src.models.auto_test.auto_test import AutoTest  # noqa
from src.models.auto_test.auto_test_environment import AutoTestEnvironment  # noqa
from src.models.auto_test.auto_test_history import AutoTestHistory  # noqa
from src.models.auto_test.test_run import TestRunHistory  # noqa
from src.models.script_runner.script import Script  # noqa
from src.models.script_runner.script_history import ScriptHistory  # noqa
from src.models.user import User  # noqa
