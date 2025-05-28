import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.database import delete_tables, create_tables, async_engine
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async_engine.echo = False
    await delete_tables()
    print("Удаление таблиц")
    await create_tables()
    print("Создание таблиц")
    async_engine.echo = True
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

static_dir = os.path.join(Path(__file__).resolve().parents[0], "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
