from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    id: int
    email: EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SAuthorized(BaseModel):
    access_token: str
