from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SearchHistoryORM(Base):
    __tablename__ = "search_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    count: Mapped[int] = mapped_column(default=1)
