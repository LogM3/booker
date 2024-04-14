from sqlalchemy import Result, Select
from sqlalchemy import func

from app.core.repos import BaseRepo
from app.database import sessionmaker
from app.hotels.models import Hotel
from app.bookings.models import Room, Booking
from app.hotels.schemas import SGetHotels, SGetRooms


class HotelRepo(BaseRepo[Hotel]):
    model: Hotel = Hotel

    @classmethod
    async def get_hotels_by_location(cls, data: SGetHotels) -> list[Hotel]:
        async with sessionmaker() as session:
            booked_rooms = Select(cls.model.id, func.count('*')).select_from(
                cls.model
            ).join(Room, cls.model.id == Room.hotel_id).join(
                Booking, Room.id == Booking.room_id
            ).where(
                (data.date_from <= Booking.date_to) &
                (data.date_to >= Booking.date_from)
            ).group_by(cls.model.id).cte('booked_rooms')

            hotel_info = Select(
                cls.model.id,
                cls.model.name,
                cls.model.location,
                cls.model.services,
                cls.model.rooms_quantity,
                cls.model.image_id,
                (cls.model.rooms_quantity - func.coalesce(
                    booked_rooms.c.count, 0
                )).label('rooms_left')
            ).select_from(cls.model).outerjoin(
                booked_rooms, booked_rooms.c.id == cls.model.id
            ).where(cls.model.location.like(f'%{data.location}%')).cte(
                'hotel_info'
            )
            hotel_info = Select('*').select_from(hotel_info).where(
                hotel_info.c.rooms_left > 0
            ).order_by(hotel_info.c.id)
            result: Result = await session.execute(hotel_info)
            return result.mappings().all()


class RoomRepo(BaseRepo[Room]):
    model: Room = Room

    @classmethod
    async def get_room_price_by_id(cls, room_id: int) -> int:
        async with sessionmaker() as session:
            room_price = Select(cls.model.price).select_from(cls.model).where(
                cls.model.id == room_id
            )
            result: Result = await session.execute(room_price)
            return result.scalar()

    @classmethod
    async def get_rooms_by_hotel(cls, data: SGetRooms) -> list[Room]:
        async with sessionmaker() as session:
            booked_rooms = Select(
                cls.model.id, func.count('*').label('booked_rooms')
            ).select_from(cls.model).join(
                Booking, cls.model.id == Booking.room_id
            ).where(
                (cls.model.hotel_id == data.hotel_id) &
                ((data.date_to >= Booking.date_from) &
                 (data.date_from <= Booking.date_to))
            ).group_by(cls.model.id).cte('booked_rooms')
            rooms = Select(
                cls.model.id,
                cls.model.hotel_id,
                cls.model.name,
                cls.model.description,
                cls.model.services,
                cls.model.quantity,
                cls.model.image_id,
                cls.model.price,
                ((data.date_to - data.date_from).days * cls.model.price).label(
                    'total_cost'
                ),
                (cls.model.quantity - func.coalesce(
                    booked_rooms.c.booked_rooms,
                    0
                )).label('rooms_left')
            ).select_from(cls.model).outerjoin(
                booked_rooms, cls.model.id == booked_rooms.c.id
            ).where(cls.model.hotel_id == data.hotel_id).order_by(
                cls.model.id
            )

            result: Result = await session.execute(rooms)
            return result.mappings().all()
