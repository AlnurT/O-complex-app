from datetime import datetime

from pytz import timezone
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.schemas.table import STableRead


class SReservationAdd(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: str = Field(examples=["2025-05-5 15:30"])
    duration_minutes: int

    @field_validator('reservation_time')
    def check_correct_date(cls, time: str) -> str:
        try:
            date_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Неверный формат даты брони",
            )

        date_time = date_time.replace(tzinfo=timezone("Europe/Moscow"))
        time_now = datetime.now(timezone("Europe/Moscow"))

        if date_time < time_now:
            raise HTTPException(
                status_code=400,
                detail="Нельзя поставить бронь на прошедшее время",
            )

        return time


class SReservationRead(SReservationAdd):
    id: int
    reservation_time: datetime = Field(examples=["2025-05-5 15:30"])

    @field_validator('reservation_time')
    def check_correct_date(cls, time: datetime) -> datetime:
        return time

    model_config = ConfigDict(from_attributes=True)


class SReservationStatus(BaseModel):
    table: STableRead
    reservation: SReservationRead
    status: bool = True
