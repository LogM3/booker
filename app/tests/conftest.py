from asyncio import AbstractEventLoop, get_event_loop_policy
from datetime import datetime
import json
from typing import List
import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, sessionmaker, engine
from app.bookings.models import Booking, Room
from app.hotels.models import Hotel
from app.users.models import User


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'
    MODELS: List[Base] = [User, Hotel, Room, Booking]

    def open_mock_json(model: Base) -> list[dict]:
        with open(
            f'app/tests/mock_{model.__tablename__}.json',
            'r',
            encoding='UTF-8'
        ) as file:
            return json.load(file)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with sessionmaker() as session:
        for model_to_insert in MODELS:
            models_from_file: list[dict] = open_mock_json(model_to_insert)

            for model in models_from_file:
                if 'date_from' and 'date_to' in model.keys():
                    model["date_from"] = datetime.fromisoformat(
                        model.get("date_from")
                    )
                    model["date_to"] = datetime.fromisoformat(
                        model.get("date_to")
                    )

            query = insert(model_to_insert).values(models_from_file)
            await session.execute(query)
        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    loop: AbstractEventLoop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
