from typing import AsyncIterator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, main, models, schemas
from src.cache.connection import Redis, redis
from src.core.config import settings
from src.db.session import SessionLocal
from src.modules.auto_test.collector import Collector

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")


async def get_db() -> AsyncIterator[AsyncSession]:
    try:
        async with SessionLocal() as session:
            yield session
    finally:
        await session.close()


async def get_redis() -> Redis:
    return await redis.get_connection()


def get_autotest_collector() -> Collector:
    return main.app.state.collector


async def get_user(session: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(session, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
