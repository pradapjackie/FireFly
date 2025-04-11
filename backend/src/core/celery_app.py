import asyncio

from celery import Celery

from src.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    include=["src.tasks"],
)

celery_app.conf.task_default_queue = "main-queue"
celery_inspect = celery_app.control.inspect()


def get_max_celery_concurrency() -> int:
    stats = celery_inspect.stats()
    max_concurrency = 0
    for info in stats.values():
        # One task can be taken by Celery to process a heartbeat.
        max_concurrency += info["pool"]["max-concurrency"] - 1
    return max_concurrency


def get_current_celery_capacity_sync() -> int:
    active_tasks = sum(len(tasks) for tasks in celery_inspect.active().values())
    max_concurrency = get_max_celery_concurrency()
    return max_concurrency - active_tasks


async def get_current_celery_capacity() -> int:
    return await asyncio.to_thread(get_current_celery_capacity_sync)
