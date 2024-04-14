from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()

    booking = relationship('Booking', back_populates='user')

    def __str__(self) -> str:
        return f'Пользователь {self.email}'
