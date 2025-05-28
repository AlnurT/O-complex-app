import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    mock_fetch_cities = AsyncMock()
    mock_fetch_weather = AsyncMock()
    mock_cities_db = MagicMock()

    monkeypatch.setattr("app.routers.fetch_cities", mock_fetch_cities)
    monkeypatch.setattr("app.routers.fetch_weather", mock_fetch_weather)
    monkeypatch.setattr("app.routers.CitiesDB", mock_cities_db)

    return {
        "fetch_cities": mock_fetch_cities,
        "fetch_weather": mock_fetch_weather,
        "cities_db": mock_cities_db,
    }
