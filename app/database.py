from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


engine: AsyncEngine = create_async_engine(
    settings.database_url,
    **settings.database_params
)

sessionmaker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
