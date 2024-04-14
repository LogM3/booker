from sqladmin import ModelView

from app.bookings.models import Booking, Room
from app.hotels.models import Hotel
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]

    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [Booking.user,
                                                           Booking.room]
    column_sortable_list = column_list[:-2]

    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-address-card"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.booking,
                                                        Room.hotel]
    column_sortable_list = column_list[:-2]

    can_delete = False
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.room]
    column_sortable_list = column_list[:-1]

    can_delete = False
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-building"
