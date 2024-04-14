import asyncio
from fastapi import Depends, Response
from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.schemas import (
    SBaseHotel,
    SGetHotels,
    SGetRooms,
    SHotel,
    SRooms
)
from app.hotels.services import HotelService, RoomService


router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('/{location}')
@cache(20)
async def get_hotels_by_location(data: SGetHotels = Depends()) -> list[SHotel]:
    await asyncio.sleep(3)
    return await HotelService.get_hotels_by_location(data)


@router.get('/id/{hotel_id}')
async def get_hotel(hotel_id: int) -> SBaseHotel:
    hotel = await HotelService.get_hotel_by_id(hotel_id)
    if not hotel:
        return Response(status_code=404)
    return hotel


@router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(data: SGetRooms = Depends()) -> list[SRooms]:
    return await RoomService.get_rooms_by_hotel(data)
