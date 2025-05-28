import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.crud import CitiesDB
from app.schemas import SWeather, SHistoryRead
from app.utils import fetch_weather, fetch_cities

router = APIRouter(
    tags=["Погода"],
)

templates_dir = os.path.join(
    Path(__file__).resolve().parents[0],
    "templates",
)
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    prev_city = request.cookies.get("last_city")
    message = ""
    if prev_city:
        message = f"Хотите посмотреть погоду в городе {prev_city}?"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": message,
        "prev_city": prev_city,
    })


@router.get("/cities")
async def get_cities(city: str = "") -> list:
    cities = await fetch_cities(city)
    return cities


@router.get("/weather", summary="Прогноз погоды")
async def get_city_weather(city: str, response: Response) -> SWeather:
    try:
        weather = await fetch_weather(city)

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
    return weather


@router.get("/requests/all", summary="Число запросов по всем городам")
async def get_cities_requests() -> list[SHistoryRead]:
    cities = await CitiesDB.count_cities_requests()

    if not cities:
        raise HTTPException(
            status_code=400,
            detail="Запросов на погоду в городах ещё не было",
        )

    return cities


@router.get("/requests", summary="Число запросов по одному городу")
async def get_city_requests(city: str) -> SHistoryRead:
    city_model = await CitiesDB.count_city_requests(city)

    if not city_model:
        raise HTTPException(
            status_code=400,
            detail=f"Запросов на погоду в городе {city} ещё не было",
        )

    return city_model
