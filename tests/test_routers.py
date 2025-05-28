from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_cities_returns_list(client, monkeypatch):
    fetch_cities_mock = AsyncMock(return_value=["Moscow", "Almaty"])
    monkeypatch.setattr("app.routers.weather.fetch_cities", fetch_cities_mock)
    response = client.get("/cities?city=Moscow")

    assert response.status_code == 200
    assert response.json() == ["Moscow", "Almaty"]


@pytest.mark.asyncio
async def test_get_city_weather_success(client, monkeypatch):
    weather_data = {
        "country": "Russia",
        "city": "Moscow",
        "temperature": 20,
        "windspeed": 10,
    }
    monkeypatch.setattr("app.routers.weather.fetch_weather",
                        AsyncMock(return_value=weather_data))
    mock_add_count = AsyncMock()
    monkeypatch.setattr("app.routers.weather.CitiesDB.add_count_city_requests",
                        mock_add_count)
    response = client.get("/weather?city=Moscow")

    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "Russia"
    assert data["city"] == "Moscow"
    assert data["temperature"] == 20
    assert data["windspeed"] == 10
    assert response.cookies.get("last_city") == "Moscow"

    mock_add_count.assert_awaited_with("Moscow")


@pytest.mark.asyncio
async def test_get_city_weather_not_found(client, monkeypatch):
    monkeypatch.setattr("app.routers.weather.fetch_weather",
                        AsyncMock(side_effect=KeyError))
    response = client.get("/weather?city=A")

    assert response.status_code == 404
    assert response.json()["detail"] == "Город A не найден"


@pytest.mark.asyncio
async def test_get_city_weather_no_access(client, monkeypatch):
    monkeypatch.setattr("app.routers.weather.fetch_weather",
                        AsyncMock(side_effect=ValueError))
    response = client.get("/weather?city=Moscow")

    assert response.status_code == 404
    assert response.json()["detail"] == "Погода недоступна"


@pytest.mark.asyncio
async def test_get_requests_all_success(client, monkeypatch):
    cities_data = [
        {"id": 1, "city": "Moscow", "count": 10},
        {"id": 2, "city": "Almaty", "count": 5}
    ]
    monkeypatch.setattr("app.routers.requests.CitiesDB.count_cities_requests",
                        AsyncMock(return_value=cities_data))
    response = client.get("/city_requests/all")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["city"] == "Moscow"
    assert data[0]["count"] == 10
    assert data[1]["city"] == "Almaty"
    assert data[1]["count"] == 5


@pytest.mark.asyncio
async def test_get_requests_all_empty(client, monkeypatch):
    monkeypatch.setattr("app.routers.requests.CitiesDB.count_cities_requests",
                        AsyncMock(return_value=[]))
    response = client.get("/city_requests/all")

    assert response.status_code == 400
    assert response.json()["detail"] == \
           "Запросов на погоду в городах ещё не было"


@pytest.mark.asyncio
async def test_get_city_requests_success(client, monkeypatch):
    city_data = {"id": 1, "city": "Moscow", "count": 10}
    monkeypatch.setattr("app.routers.requests.CitiesDB.count_city_requests",
                        AsyncMock(return_value=city_data))
    response = client.get("/city_requests?city=Moscow")

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Moscow"
    assert data["count"] == 10


@pytest.mark.asyncio
async def test_get_city_requests_not_found(client, monkeypatch):
    monkeypatch.setattr("app.routers.requests.CitiesDB.count_city_requests",
                        AsyncMock(return_value=None))
    response = client.get("/city_requests?city=A")

    assert response.status_code == 400
    assert response.json()["detail"] == \
           "Запросов на погоду в городе A ещё не было"
