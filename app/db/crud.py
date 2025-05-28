from sqlalchemy import select

from app.db.database import async_session
from app.db.models import SearchHistoryORM
from app.schemas import SHistoryRead


class CitiesDB:
    @classmethod
    async def count_cities_requests(cls) -> list[SHistoryRead]:
        async with async_session() as session:
            query = select(SearchHistoryORM)
            result = await session.execute(query)
            city_models = result.scalars().all()
            cities = [
                SHistoryRead.model_validate(city_model)
                for city_model in city_models
            ]
            return cities

    @classmethod
    async def count_city_requests(cls, city: str) -> SHistoryRead | None:
        async with async_session() as session:
            query = select(SearchHistoryORM).filter_by(city=city)
            result = await session.scalar(query)
            if result:
                return SHistoryRead.model_validate(result)

            return None

    @classmethod
    async def add_count_city_requests(cls, city: str) -> None:
        async with async_session() as session:
            query = select(SearchHistoryORM).filter_by(city=city)
            result = await session.scalar(query)

            if not result:
                result = SearchHistoryORM(city=city)
                session.add(result)
            else:
                result.count += 1

            await session.commit()
