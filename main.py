import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import delete_tables, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Создание таблиц")
    yield
    await delete_tables()
    print("Удаление таблиц")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_weather():
    return {'message': "Hellow World"}


# async def ap():
#     await create_tables()
#     print("Создание таблиц")
#     await delete_tables()
#     print("Удаление таблиц")
#
# asyncio.run(ap())

