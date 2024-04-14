from datetime import date

from app.bookings.models import Booking, Room
from app.core.repos import BaseRepo
from app.database import sessionmaker

from sqlalchemy import Select, func
from sqlalchemy.engine.result import ChunkedIteratorResult as Result


class BookingRepo(BaseRepo[Booking]):
    model: Booking = Booking

    @classmethod
    async def get_user_bookings(cls, user_id: int) -> list[Booking]:
        async with sessionmaker() as session:
            user_bookings = Select(
                cls.model.room_id,
                cls.model.user_id,
                cls.model.date_from,
                cls.model.date_to,
                cls.model.price,
                cls.model.total_cost,
                cls.model.total_days,
                Room.image_id,
                Room.name,
                Room.description,
                Room.services
            ).outerjoin(Room, cls.model.room_id == Room.id).where(
                cls.model.user_id == user_id
            ).order_by(cls.model.date_from)

            result: Result = await session.execute(user_bookings)
            return result.mappings().all()

    @classmethod
    async def check_room_availability(
        cls,
        room_id: int,
        date_from: date,
        date_to: date
    ) -> int:
        async with sessionmaker() as session:
            booked_rooms = Select(cls.model).select_from(cls.model).where(
                (cls.model.room_id == room_id) &
                (cls.model.date_from <= date_to) &
                (cls.model.date_to >= date_from)
            ).cte('booked_rooms')

            rooms_left = Select(
                Room.quantity - func.count(booked_rooms.c.room_id)
            ).select_from(Room).where(
                Room.id == room_id
            ).outerjoin(
                booked_rooms, booked_rooms.c.room_id == Room.id
            ).group_by(Room.quantity, booked_rooms.c.room_id)

            result: Result = await session.execute(rooms_left)
            return result.scalar()

    @classmethod
    async def delete_booking(cls, booking_id: int, user_id: int) -> bool:
        async with sessionmaker() as session:
            booking = Select(cls.model).select_from(cls.model).where(
                cls.model.id == booking_id,
                cls.model.user_id == user_id
            )
            result: Result = await session.execute(booking)
            result = result.scalar_one_or_none()
            if not result:
                return False
            await session.delete(result)
            await session.commit()
            return True
