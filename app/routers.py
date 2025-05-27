# from typing import Annotated
#
# from fastapi import APIRouter, Depends, HTTPException
#
# from app.crud import TableRepository
# from app.schemas import STableRead, STableAdd, STableStatus
#
# tables_router = APIRouter(
#     prefix="/table",
#     tags=["Столики"],
# )
#
#
# @tables_router.get("", summary="Cписок всех столиков")
# async def get_tables() -> list[STableRead]:
#     tables = await TableRepository.find_all()
#     return tables
#
#
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
