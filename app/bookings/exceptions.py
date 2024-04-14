from app.core.exceptions import BaseException


class BookingDateException(BaseException):
    status_code = 400
    detail = 'Date of check-out must be greater, then date of check-in!'


class RoomCannotBeBookedException(BaseException):
    status_code = 400
    detail = 'This room is not available for booking!'


class BookingCannotBeDeletedException(BaseException):
    status_code = 404
    detail = 'This booking cannot be found!'
