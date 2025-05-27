from pydantic import BaseModel, ConfigDict


class SHistoryAdd(BaseModel):
    user_id: str
    city: str
    count: int


class SHistoryRead(SHistoryAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
