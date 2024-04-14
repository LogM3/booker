from fastapi import Depends, Response, APIRouter, status

from app.users.dependencies import get_current_user
from app.users.exceptions import (
    EmailAlreadyExistsException,
    WrongCredentialsException
)
from app.users.models import User
from app.users.services import AuthService
from app.users.schemas import SAuthorized, SUser, SUserAuth


router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация & Пользователи']
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def user_register(user_data: SUserAuth) -> SUser:
    service: AuthService = AuthService(user_data)
    user: User = await service.register()
    if not user:
        raise EmailAlreadyExistsException
    return user


@router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(response: Response, user_data: SUserAuth) -> SAuthorized:
    service: AuthService = AuthService(user_data)
    user: User = await service.authorize()
    if not user:
        raise WrongCredentialsException()
    access_token: str = AuthService.encode_access_token(user)
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return SAuthorized(access_token=access_token)


@router.post('/logout')
async def logout(response: Response) -> None:
    response.delete_cookie('booking_access_token')


@router.get('/me')
async def get_current_user(user: User = Depends(get_current_user)) -> SUser:
    return user
