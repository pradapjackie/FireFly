from fastapi import APIRouter

from src.api.endpoints import health, load_test_runner, login, script_runner, test_runner, users

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(test_runner.router, prefix="/autotest", tags=["autotest"])
api_router.include_router(script_runner.router, prefix="/script", tags=["script runner"])
api_router.include_router(load_test_runner.router, prefix="/load_test", tags=["load test"])
api_router.include_router(health.router, tags=["health"])
