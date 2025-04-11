from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_user),
) -> Any:
    if not current_user:
        return
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, dependencies=[Depends(deps.get_user)])
async def create_user(*, db: AsyncSession = Depends(deps.get_db), user_in: schemas.UserCreate) -> Any:
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(400, "The user with this username already exists in the system.")
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
async def read_user_me(current_user: models.User = Depends(deps.get_user)) -> Any:
    return current_user


@router.get("/{user_id}", response_model=schemas.User, dependencies=[Depends(deps.get_user)])
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(deps.get_db)) -> Any:
    return await crud.user.get(db, id=user_id)


@router.put("/{user_id}", response_model=schemas.User, dependencies=[Depends(deps.get_user)])
async def update_user(*, db: AsyncSession = Depends(deps.get_db), user_id: int, user_in: schemas.UserUpdate) -> Any:
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(404, "The user with this username does not exist in the system")
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
