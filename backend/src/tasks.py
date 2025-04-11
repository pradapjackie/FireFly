from src.core.celery_app import celery_app
from src.modules.auto_test.manager import TestManager
from src.modules.load_test_runner.supervisor import LoadTestSupervisor
from src.modules.load_test_runner.worker_manager import LoadTestWorkerManager


@celery_app.task(ignore_result=True)
def run_tests(run_id: str):
    TestManager(run_id).run_all_sync()


@celery_app.task(ignore_result=True)
def start_load_task(load_test_id: str, execution_id: str, worker_id: str):
    LoadTestWorkerManager(load_test_id, execution_id, worker_id).start_sync()


@celery_app.task(ignore_result=True)
def start_load_test_supervisor(load_test_id: str, execution_id: str):
    LoadTestSupervisor(load_test_id, execution_id).start_sync()
