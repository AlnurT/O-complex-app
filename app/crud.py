# from sqlalchemy import select
#
# from app.database import async_session
# from app.models import TableORM
# from app.schemas import STableRead, STableAdd
#
#
# class TableRepository:
#     @classmethod
#     async def find_all(cls) -> list[STableRead]:
#         async with async_session() as session:
#             query = select(TableORM)
#             result = await session.execute(query)
#             table_models = result.scalars().all()
#             tables = [
#                 STableRead.model_validate(table_model)
#                 for table_model in table_models
#             ]
#             return tables
#
#     @classmethod
#     async def check_table_name(cls, table_name: str) -> bool:
#         async with async_session() as session:
#             query = select(TableORM).filter_by(name=table_name)
#             table = await session.scalar(query)
#             return True if table else False
#
#     @classmethod
#     async def find_one(cls, table_id: int) -> STableRead | None:
#         async with async_session() as session:
#             query = select(TableORM).filter_by(id=table_id)
#             table = await session.scalar(query)
#             if table:
#                 return STableRead.model_validate(table)
#
#             return
#
#     @classmethod
#     async def add_one(cls, data: STableAdd) -> STableRead:
#         async with async_session() as session:
#             table_dict = data.model_dump()
#             table = TableORM(**table_dict)
#
#             session.add(table)
#             await session.flush()
#             await session.commit()
#             return STableRead.model_validate(table)
#
#     @classmethod
#     async def delete_one(cls, table_id: int) -> STableRead | bool:
#         async with async_session() as session:
#             query = select(TableORM).filter_by(id=table_id)
#             table = await session.scalar(query)
#
#             if not table:
#                 return False
#
#             await session.delete(table)
#             await session.commit()
#             return STableRead.model_validate(table)
