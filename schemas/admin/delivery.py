from decimal import Decimal

from pydantic import BaseModel, Field


class DeliveryBaseSchema(BaseModel):
    radius_from: float = Field(
        default=..., description="Radius from in kilometers", gt=0
    )
    radius_to: float = Field(default=..., description="Radius to in kilometers", gt=0)

    delivery_time: int = Field(
        default=..., description="Delivery time in minutes", gt=0
    )

    price: Decimal = Field(default=..., description="Price", gt=0)


class DeliveryCreateSchema(DeliveryBaseSchema):
    pass


class DeliveryUpdateSchema(DeliveryBaseSchema):
    pass
