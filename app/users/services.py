from datetime import timedelta, datetime
from passlib.context import CryptContext

import jwt

from app.config import settings as s
from app.core.services import BaseService
from app.users.models import User
from app.users.repos import UserRepo
from app.users.schemas import SUserAuth


class BaseAuthService(BaseService):
    """Содержит базовые методы для аутентификации"""

    repo: UserRepo = UserRepo
    crypto: CryptContext = CryptContext(
            schemes=['bcrypt'],
            deprecated='auto'
    )

    def get_password_hash(self, password: str) -> str:
        """Хэширует переданный пароль"""

        return self.crypto.hash(password)

    def compare_passwords(
        self,
        password: str,
        hashed_password: str
    ) -> bool:
        """Сравнивает переданный пароль с хэшированным пользователя"""

        return self.crypto.verify(password, hashed_password)

    @staticmethod
    def encode_access_token(user: User) -> str:
        """Создает и возвращает токен доступа для переданного пользователя"""

        expire: datetime = datetime.utcnow() + timedelta(
            minutes=s.JWT_EXPIRE_MINUTES)
        return jwt.encode(
            {'sub': user.id, 'exp': expire},
            s.SECRET_KEY,
            s.JWT_ALGORITHM
        )


class AuthService(BaseAuthService):
    """Содержит методы регистрации и аутентификации пользователя"""

    def __init__(
        self,
        user_data: SUserAuth
    ) -> None:
        self.email: str = user_data.email
        self.password: str = user_data.password

    async def register(self) -> User:
        """Создает и возврашает нового пользователя"""

        if await self.repo.get_user_by_email(self.email):
            return None

        user_data: dict = {
            'email': self.email,
            'hashed_password': self.get_password_hash(self.password)
        }
        user: User = await self.repo.create(**user_data)
        return user

    async def authorize(self) -> User | None:
        """Проверяет уч. данные и возвращает объект пользователя"""

        user: User = await self.repo.get_user_by_email(self.email)
        if user and self.compare_passwords(
            self.password,
            user.hashed_password
        ):
            return user
        return None
