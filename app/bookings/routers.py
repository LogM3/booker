from fastapi import Depends
from fastapi.routing import APIRouter

from app.bookings.exceptions import BookingCannotBeDeletedException
from app.bookings.services import BookingService
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user, get_token_user_id
from app.bookings.schemas import SBooking, SCreateBooking
from app.users.models import User


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get('')
async def get_bookings(
    user_id: int = Depends(get_token_user_id)
) -> list[SBooking]:
    return await BookingService.get_user_bookings(user_id)


@router.post('')
async def add_booking(
    user: User = Depends(get_current_user),
    booking_data: SCreateBooking = Depends()
) -> SCreateBooking:
    booking: dict = SCreateBooking.model_validate(
        await BookingService.create_booking(
            user.id,
            booking_data
        )
    ).model_dump()
    send_booking_confirmation_email.delay(booking, user.email)
    return booking


@router.delete('/{booking_id}', status_code=204)
async def delete_booking(
    booking_id: int,
    user: User = Depends(get_current_user)
) -> None:
    result: bool = await BookingService.delete_booking(booking_id, user)
    if not result:
        raise BookingCannotBeDeletedException()
