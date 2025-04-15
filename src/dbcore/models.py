from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.dbcore.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class TableORM(Base):
    __tablename__ = "table"

    id: Mapped[intpk]
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]


class ReservationORM(Base):
    __tablename__ = "reservation"

    id: Mapped[intpk]
    customer_name: Mapped[str]
    table_id: Mapped[int] = \
        mapped_column(ForeignKey("table.id", ondelete="CASCADE"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]
