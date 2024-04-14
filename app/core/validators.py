from datetime import date

from pydantic import ValidationInfo

from app.bookings.exceptions import BookingDateException


def validate_date_to(v: date, info: ValidationInfo) -> date:
    if v <= info.data.get('date_from'):
        raise BookingDateException()
    return v
