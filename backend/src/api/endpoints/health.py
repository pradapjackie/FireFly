from fastapi import APIRouter

from src import schemas
from src.core.config import settings

router = APIRouter()


@router.get("/version/")
async def version() -> schemas.Version:
    return schemas.Version(version=settings.PROJECT_VERSION)
