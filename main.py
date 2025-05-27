from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import delete_tables, create_tables
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Создание таблиц")
    yield
    await delete_tables()
    print("Удаление таблиц")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
