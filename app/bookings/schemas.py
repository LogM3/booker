from datetime import date
from pydantic import BaseModel, field_validator, ValidationInfo

from app.core.validators import validate_date_to


class SBooking(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str
    services: list


class SCreateBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    class Config:
        from_attributes = True

    @field_validator('date_to')
    @classmethod
    def validate_date_to(cls, v: date, info: ValidationInfo) -> date:
        return validate_date_to(v, info)
