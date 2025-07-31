from decimal import Decimal

from pydantic import BaseModel, Field


class DeliveryBaseSchema(BaseModel):
    radius_from: float | None = Field(
        default=None, description="Radius from in kilometers", gt=0
    )
    radius_to: float | None = Field(
        default=None, description="Radius to in kilometers", gt=0
    )

    delivery_time: int | None = Field(
        default=None, description="Delivery time in minutes", gt=0
    )

    price: Decimal | None = Field(default=None, description="Price", gt=0)


class DeliveryCreateSchema(DeliveryBaseSchema):
    pass


class DeliveryUpdateSchema(DeliveryBaseSchema):
    pass
