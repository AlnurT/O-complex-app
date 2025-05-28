import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

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

static_dir = os.path.join(Path(__file__).resolve().parents[0], "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
