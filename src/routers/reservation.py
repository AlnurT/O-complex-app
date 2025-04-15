from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.repository.reservation import ReservationRepository
from src.repository.table import TableRepository
from src.schemas.reservation import SReservationRead, SReservationStatus, \
    SReservationAdd

reservations_router = APIRouter(
    prefix="/reservation",
    tags=["Бронирование"],
)


@reservations_router.get("", summary="Cписок всех броней")
async def get_reservations() -> list[SReservationRead]:
    reservations = await ReservationRepository.find_all()
    return reservations


@reservations_router.post("", summary="Cоздать новую бронь")
async def add_reservation(
        reservation: Annotated[SReservationAdd, Depends()],
) -> SReservationStatus:
    table = await TableRepository.find_one(reservation.table_id)

    if table is None:
        raise HTTPException(
            status_code=404,
            detail="Такого столика не существует",
        )

    if not await ReservationRepository.check_reservation_time(reservation):
        raise HTTPException(
            status_code=400,
            detail="Время занято",
        )

    reserv = await ReservationRepository.add_one(reservation)
    return {"table": table, "reservation": reserv, "status": True}


@reservations_router.delete("/{reserv_id}", summary="Удалить бронь")
async def delete_table(reserv_id: int) -> SReservationStatus:
    reserv = await ReservationRepository.delete_one(reserv_id)

    if not reserv:
        raise HTTPException(
            status_code=404,
            detail=f"Брони c id = {reserv_id} не существует",
        )

    table = await TableRepository.find_one(reserv.table_id)
    return {"table": table, "reservation": reserv, "status": True}
