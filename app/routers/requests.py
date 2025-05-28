from fastapi import APIRouter, HTTPException

from app.db.crud import CitiesDB
from app.schemas import SHistoryRead

city_request = APIRouter(
    prefix="/city_requests",
    tags=["Запросы"],
)


@city_request.get("/all", summary="Число запросов по всем городам")
async def get_cities_requests() -> list[SHistoryRead]:
    cities = await CitiesDB.count_cities_requests()

    if not cities:
        raise HTTPException(
            status_code=400,
            detail="Запросов на погоду в городах ещё не было",
        )

    return cities


@city_request.get("", summary="Число запросов по одному городу")
async def get_city_requests(city: str) -> SHistoryRead:
    city_model = await CitiesDB.count_city_requests(city)

    if not city_model:
        raise HTTPException(
            status_code=400,
            detail=f"Запросов на погоду в городе {city} ещё не было",
        )

    return city_model
