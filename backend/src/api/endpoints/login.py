from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps
from src.core import security

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=schemas.User)
async def test_token(current_user: models.User = Depends(deps.get_user)) -> Any:
    return current_user


@router.post("/signup")
async def sign_up(request: schemas.SignUpRequest, db: AsyncSession = Depends(deps.get_db)):
    user = await crud.user.get_by_name_or_email(db, full_name=request.full_name, email=request.email)
    if user:
        raise HTTPException(400, "The user with this Name or Email already exists.")
    user = await crud.user.create(db, obj_in=schemas.UserCreate(**request.model_dump()))
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }
