import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.schemas import SWeather
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

    response.set_cookie(key="last_city", value=city)
    return weather


# @tables_router.post("", summary="Cоздать новый столик")
# async def add_table(
#         table: Annotated[STableAdd, Depends()],
# ) -> STableStatus:
#     if await TableRepository.check_table_name(table.name):
#         raise HTTPException(
#             status_code=400,
#             detail="Столик с таким именем уже существует",
#         )
#
#     table = await TableRepository.add_one(table)
#     return {"data": table, "status": True}
#
#
# @tables_router.delete("/{table_id}", summary="Удалить столик")
# async def delete_table(table_id: int) -> STableStatus:
#     table = await TableRepository.delete_one(table_id)
#
#     if not table:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Столика c id = {table_id} не существует",
#         )
#
#     return {"data": table, "status": True}
