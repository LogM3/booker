from fastapi import status

from app.core.exceptions import BaseException


class AuthException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Unauthorized'


class EmailAlreadyExistsException(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'This email is already registered!'


class WrongCredentialsException(AuthException):
    detail = 'Wrong credentials!'


class WrongPasswordException(AuthException):
    detail = 'Provided password is not valid!'


class InvalidTokenException(AuthException):
    def __init__(self, detail: str):
        self.detail = detail


class UserNotExists(AuthException):
    detail = 'This user is not exists'
