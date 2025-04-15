from pydantic import BaseModel, ConfigDict, Field


class STableAdd(BaseModel):
    name: str = Field(examples=["Table 1", "Стол 1"])
    seats: int = Field(gt=0)
    location: str = Field(examples=["зал у окна", "терраса"])


class STableRead(STableAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class STableStatus(BaseModel):
    data: STableRead
    status: bool = True
