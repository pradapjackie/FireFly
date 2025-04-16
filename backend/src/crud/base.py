from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10000) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def create_multi(self, db: AsyncSession, *, objects_in: List[CreateSchemaType]) -> None:
        for obj_in in objects_in:
            query = insert(self.model).values(obj_in.model_dump())
            await db.execute(query)
        await db.commit()

    @staticmethod
    async def update(
        db: AsyncSession, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def truncate(self, db: AsyncSession):
        await db.execute(text(f"TRUNCATE TABLE {self.model.__tablename__}"))
        await db.commit()

    async def delete_all(self, db: AsyncSession):
        await db.execute(delete(self.model))
        await db.commit()
