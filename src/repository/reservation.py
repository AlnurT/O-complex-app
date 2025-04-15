from datetime import datetime, timedelta

from sqlalchemy import select

from src.dbcore.database import async_session
from src.dbcore.models import ReservationORM
from src.schemas.reservation import SReservationRead, SReservationAdd


class ReservationRepository:
    @classmethod
    async def find_all(cls) -> list[SReservationRead]:
        async with async_session() as session:
            query = select(ReservationORM)
            result = await session.execute(query)
            reserv_models = result.scalars().all()
            reservations = [
                SReservationRead.model_validate(reserv)
                for reserv in reserv_models
            ]
            return reservations

    @classmethod
    async def check_reservation_time(cls, data: SReservationAdd) -> bool:
        async with async_session() as session:
            query = select(ReservationORM).filter_by(table_id=data.table_id)
            result = await session.execute(query)
            reserv_models = result.scalars().all()
            check_time = datetime.strptime(
                data.reservation_time, '%Y-%m-%d %H:%M',
            )
            end_check_time = check_time + \
                             timedelta(minutes=data.duration_minutes)

            for reserv in reserv_models:
                start_time = reserv.reservation_time
                end_time = start_time + \
                           timedelta(minutes=reserv.duration_minutes)

                if not (end_check_time <= start_time or
                        check_time >= end_time):
                    return False

            return True

    @classmethod
    async def add_one(cls, data: SReservationAdd) -> SReservationRead:
        async with async_session() as session:
            reserv_dict = data.model_dump()
            reserv_dict["reservation_time"] = datetime.strptime(
                data.reservation_time, '%Y-%m-%d %H:%M',
            )
            reserv = ReservationORM(**reserv_dict)

            session.add(reserv)
            await session.flush()
            await session.commit()
            return SReservationRead.model_validate(reserv)

    @classmethod
    async def delete_one(cls, reserv_id: int) -> SReservationRead | bool:
        async with async_session() as session:
            query = select(ReservationORM).filter_by(id=reserv_id)
            reservation = await session.scalar(query)

            if not reservation:
                return False

            await session.delete(reservation)
            await session.commit()
            return SReservationRead.model_validate(reservation)
