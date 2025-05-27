from fastapi import APIRouter, HTTPException

from app.schemas import SWeather
from app.utils import fetch_weather

router = APIRouter(
    tags=["Погода"],
)


@router.get("/weather", summary="Прогноз погоды")
async def get_city_weather(city: str) -> SWeather:
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

    return weather


@router.get("/", summary="Краткое описание")
async def get_weather():
    return {'message': "API для показа прогноза погоды"}


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
