from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from enums.order import OrderStatusEnum


class OrderFilterSchema(BaseModel):
    status: OrderStatusEnum | None = Field(default=None, description="Order status")


class OrderDishBaseSchema(BaseModel):
    dish_id: int = Field(default=..., description="Dish ID", gt=0)

    price: Decimal = Field(default=..., description="Dish price", gt=0)
    quantity: int = Field(default=..., description="Dish quantity", gt=0)


class OrderDishResponseSchema(OrderDishBaseSchema):
    id: int = Field(default=..., description="Dish ID", gt=0)

    order_id: int = Field(default=..., description="Order ID", gt=0)

    class Config:
        from_attributes = True


class OrderDishCreateSchema(OrderDishBaseSchema):
    pass


class OrderBaseSchema(BaseModel):
    check_photo_url: str | None = Field(default=None, description="Check photo URL")
    price: Decimal = Field(default=..., description="Order price", gt=0)


class OrderResponseSchema(OrderBaseSchema):
    id: int = Field(default=..., description="Order ID", gt=0)

    client_id: int = Field(default=..., description="Client ID", gt=0)

    status: OrderStatusEnum = Field(default=..., description="Order status")

    order_dishes: list[OrderDishResponseSchema] = Field(
        default_factory=list, description="Order dishes"
    )

    created_at: datetime = Field(default=..., description="Order created at")

    class Config:
        from_attributes = True


class OrderCreateSchema(OrderBaseSchema):
    order_dishes: list[OrderDishCreateSchema] = Field(
        default_factory=list, description="Order dishes"
    )


class OrderStatusSchema(BaseModel):
    value: int = Field(default=..., description="Order status value")
    name: str = Field(default=..., description="Order status name")
    description: str = Field(default=..., description="Order status description")

    class Config:
        from_attributes = True
