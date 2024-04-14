from abc import ABC
from typing import Generic, Optional, TypeVar

from app.database import sessionmaker, Base

from sqlalchemy import select, insert
from sqlalchemy.engine.result import ChunkedIteratorResult as Result

T = TypeVar('T')


class BaseRepo(ABC, Generic[T]):
    model: Optional[Base] = None

    @classmethod
    async def get_by_id(cls, model_id: int) -> Base:
        async with sessionmaker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result: Result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by) -> Optional[Base]:
        async with sessionmaker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by) -> list[Base]:
        async with sessionmaker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def create(cls, **data) -> Base:
        async with sessionmaker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result: Result = await session.execute(query)
            await session.commit()
            return result.scalar()
