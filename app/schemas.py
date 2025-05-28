from pydantic import BaseModel, ConfigDict


class SHistoryRead(BaseModel):
    id: int
    city: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class SWeather(BaseModel):
    country: str
    city: str
    temperature: float
    windspeed: float
