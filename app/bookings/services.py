from pydantic import EmailStr

from app.tasks.tasks import send_booking_confirmation_email
from app.bookings.models import Booking
from app.bookings.repos import BookingRepo
from app.bookings.exceptions import RoomCannotBeBookedException
from app.bookings.schemas import SCreateBooking
from app.core.services import BaseService
from app.hotels.repos import RoomRepo
from app.users.models import User


class RoomService(BaseService):
    repo = RoomRepo

    @classmethod
    async def get_room_price(cls, room_id: int) -> int:
        return await cls.repo.get_room_price_by_id(room_id)


class BookingService(BaseService):
    repo: BookingRepo = BookingRepo

    @classmethod
    async def get_user_bookings(cls, user_id: int) -> list[Booking]:
        return await cls.repo.get_user_bookings(user_id)

    @classmethod
    async def send_confirmation_email(
        booking: dict,
        email_to: EmailStr
    ) -> None:
        send_booking_confirmation_email.delay(booking, email_to)

    @classmethod
    async def create_booking(
        cls,
        user_id: int,
        booking_data: SCreateBooking
    ) -> Booking:
        rooms_left: int = await BookingRepo.check_room_availability(
            booking_data.room_id,
            booking_data.date_from,
            booking_data.date_to
        )
        if rooms_left <= 0:
            raise RoomCannotBeBookedException()

        room_price: int = await RoomRepo.get_room_price_by_id(
            booking_data.room_id
        )
        booking_data: dict = booking_data.model_dump()
        booking_data.update({
            'user_id': user_id,
            'price': room_price
        })
        return await BookingRepo.create(**booking_data)

    @classmethod
    async def delete_booking(cls, booking_id: int, user: User) -> bool:
        return await cls.repo.delete_booking(booking_id, user.id)
