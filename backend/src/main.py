from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.api import api_router
from src.api.deps import get_redis
from src.core.config import settings
from src.db.session import SessionLocal
from src.modules.auto_test.collector import Collector as AutoTestCollector
from src.modules.environment.env import prime_environment_cache
from src.modules.load_test_runner.collector import Collector as LoadTestCollector
from src.modules.script_runner.collector import Collector as ScriptCollector

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, openapi_url="/api/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


async def start_up_task():
    redis = await get_redis()
    prime_key = f"primed_{settings.PROJECT_VERSION}"
    if await redis.set(prime_key, "true", nx=True):
        print(f"{settings.PROJECT_VERSION} start tag priming", flush=True)
        try:
            async with SessionLocal() as db:
                auto_test_collector = AutoTestCollector()
                script_collector = ScriptCollector()
                load_test_collector = LoadTestCollector()
                await prime_environment_cache(db, redis)
                await auto_test_collector.collect_and_save_tests_in_db(db)
                await script_collector.collect_and_save_scripts_in_db(db)
                await load_test_collector.collect_and_save_load_tests_in_db(db)
        except Exception as e:
            print(f"{settings.PROJECT_VERSION} tag primed error: {e}", flush=True)
        finally:
            await db.close()
        print(f"{settings.PROJECT_VERSION} tag primed and running", flush=True)


@app.on_event("startup")
async def startup_event():
    # noinspection PyUnresolvedReferences
    app.state.collector = AutoTestCollector()
    await start_up_task()
