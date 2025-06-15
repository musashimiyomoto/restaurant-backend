from pydantic import BaseModel, Field

from enums.order import OrderStatusEnum


class OrderFilterSchema(BaseModel):
    client_id: int | None = Field(default=None, description="Client ID", gt=0)

    status: OrderStatusEnum | None = Field(default=None, description="Order status")
