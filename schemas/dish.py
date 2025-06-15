from decimal import Decimal

from pydantic import BaseModel, Field


class DishFilterSchema(BaseModel):
    category_id: int | None = Field(default=None, description="Category ID", gt=0)


class DishResponseSchema(BaseModel):
    id: int = Field(default=..., description="ID", gt=0)

    category_id: int | None = Field(default=None, description="Category ID", gt=0)

    price: Decimal = Field(default=..., description="Price", gt=0)
    weight: Decimal = Field(default=..., description="Weight", gt=0)
    photo_url: str | None = Field(default=None, description="Photo URL")
    name: str = Field(default=..., description="Name")
    description: str | None = Field(default=None, description="Description")

    class Config:
        from_attributes = True
