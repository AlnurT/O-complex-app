import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from db.database import delete_tables, create_tables, async_engine
from app.routers.weather import weather
from app.routers.requests import city_request


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
templates_dir = os.path.join(Path(__file__).resolve().parents[0], "templates")
templates = Jinja2Templates(directory=templates_dir)

static_dir = os.path.join(Path(__file__).resolve().parents[0], "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse, summary="Главная", tags=["Главная"])
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


app.include_router(weather)
app.include_router(city_request)
