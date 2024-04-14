from fastapi import HTTPException


class BaseException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
