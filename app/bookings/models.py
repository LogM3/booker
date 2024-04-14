from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey, Date, Computed


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    price: Mapped[int] = mapped_column()
    services: Mapped[dict | None] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column()
    image_id: Mapped[int] = mapped_column()

    booking = relationship('Booking', back_populates='room')
    hotel = relationship('Hotel', back_populates='room')

    def __str__(self) -> str:
        return f'Комната {self.name}'


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[str] = mapped_column(Date)
    date_to: Mapped[str] = mapped_column(Date)
    price: Mapped[int] = mapped_column()
    total_days: Mapped[int] = mapped_column(Computed('date_to - date_from'))
    total_cost: Mapped[int] = mapped_column(Computed(
        '(date_to - date_from) * price'))

    user = relationship('User', back_populates='booking')
    room = relationship('Room', back_populates='booking')

    def __str__(self) -> str:
        return f'Бронь #{self.id}'
