from datetime import date
from pydantic import BaseModel, ValidationInfo, field_validator

from app.core.validators import validate_date_to


class SBaseHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int


class SHotel(SBaseHotel):
    rooms_left: int


class SGetHotels(BaseModel):
    location: str
    date_from: date
    date_to: date

    @field_validator('date_to')
    @classmethod
    def validate_date_to(cls, v: date, info: ValidationInfo) -> date:
        return validate_date_to(v, info)


class SGetRooms(BaseModel):
    hotel_id: int
    date_from: date
    date_to: date

    @field_validator('date_to')
    @classmethod
    def validate_date_to(cls, v: date, info: ValidationInfo) -> date:
        return validate_date_to(v, info)


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int
