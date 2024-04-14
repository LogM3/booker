from fastapi import Depends, Request
import jwt

from app.users.exceptions import (
    AuthException,
    InvalidTokenException,
    UserNotExists
)
from app.config import settings
from app.users.models import User
from app.users.repos import UserRepo


def decode_token(request: Request) -> dict:
    """Декодирует токен и возвращает закодированные в нём данные"""

    token: str = request.cookies.get('booking_access_token')
    if not token:
        raise AuthException()
    try:
        data: dict = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM
        )
    except jwt.exceptions.InvalidTokenError as e:
        raise InvalidTokenException(e.args[0])
    return data


async def get_token_user_id(data: dict = Depends(decode_token)) -> int:
    """Возвращает id пользователя из токена"""

    user_id: int = data.get('sub')
    if not user_id or not await UserRepo.get_by_id(int(user_id)):
        raise UserNotExists()
    return user_id


async def get_current_user(user_id: int = Depends(get_token_user_id)) -> User:
    return await UserRepo.get_by_id(user_id)
