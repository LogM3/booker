from app.bookings.models import Room
from app.core.services import BaseService
from app.hotels.models import Hotel
from app.hotels.repos import HotelRepo, RoomRepo
from app.hotels.schemas import SGetHotels, SGetRooms


class HotelService(BaseService):
    repo: HotelRepo = HotelRepo

    @classmethod
    async def get_hotels_by_location(cls, data: SGetHotels) -> list[Hotel]:
        return await cls.repo.get_hotels_by_location(data)

    @classmethod
    async def get_hotel_by_id(cls, hotel_id: int) -> Hotel:
        return await cls.repo.get_by_id(hotel_id)


class RoomService(BaseService):
    repo: RoomRepo = RoomRepo

    @classmethod
    async def get_rooms_by_hotel(cls, data: SGetRooms) -> list[Room]:
        return await cls.repo.get_rooms_by_hotel(data)
