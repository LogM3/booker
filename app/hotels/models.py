from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON


class Hotel(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column()
    services: Mapped[dict | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column()
    image_id: Mapped[int] = mapped_column()

    room = relationship('Room', back_populates='hotel')

    def __str__(self) -> str:
        return f'Hotel {self.name}'
