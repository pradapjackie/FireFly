from typing import Any, Dict, Optional, Union

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas
from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    @staticmethod
    async def get_by_email(db: AsyncSession, *, email: str) -> Optional[models.User]:
        result = await db.execute(select(models.User).where(models.User.email == email))
        return result.scalars().first()

    async def get_by_name_or_email(self, db: AsyncSession, *, full_name: str, email: str) -> models.User | None:
        result = await db.execute(
            select(models.User).where(or_(self.model.full_name == full_name, self.model.email == email))
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email, full_name=obj_in.full_name, password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: models.User, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]
    ) -> models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[models.User]:
        user_from_db = await self.get_by_email(db, email=email)
        if not user_from_db:
            return None
        if not verify_password(password, user_from_db.password):
            return None
        return user_from_db

    @staticmethod
    def is_active(current_user: models.User) -> bool:
        return not current_user.disabled


user = CRUDUser(models.User)
