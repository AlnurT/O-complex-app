from fastapi import APIRouter, HTTPException, Response

from app.db.crud import CitiesDB
from app.schemas import SWeather
from app.utils import fetch_weather, fetch_cities

weather = APIRouter(
    tags=["Погода"],
)


@weather.get("/cities")
async def get_cities(city: str = "") -> list:
    cities = await fetch_cities(city)
    return cities


@weather.get("/weather", summary="Прогноз погоды")
async def get_city_weather(city: str, response: Response) -> SWeather:
    try:
        result = await fetch_weather(city)

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Город {city} не найден",
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Погода недоступна",
        )

    await CitiesDB.add_count_city_requests(city)
    response.set_cookie(key="last_city", value=city)
    return result
