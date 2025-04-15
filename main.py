from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.dbcore.database import delete_tables, create_tables
from src.routers.reservation import reservations_router
from src.routers.table import tables_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Создание таблиц")
    yield
    await delete_tables()
    print("Удаление таблиц")


app = FastAPI(lifespan=lifespan)
app.include_router(tables_router)
app.include_router(reservations_router)
