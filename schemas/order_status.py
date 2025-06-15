from datetime import datetime

from pydantic import BaseModel, Field

from enums.order import OrderStatusEnum


class OrderStatusResponseSchema(BaseModel):
    status: OrderStatusEnum = Field(default=..., description="Order status")

    start_date: datetime = Field(default=..., description="Start date of the status")
    end_date: datetime | None = Field(
        default=None, description="End date of the status"
    )

    changed_by_user_id: int | None = Field(
        default=None, description="ID of the user who changed the status"
    )
    changed_by_client_id: int | None = Field(
        default=None, description="ID of the client who changed the status"
    )

    duration_seconds: int | None = Field(
        default=None, description="Duration of the status in seconds"
    )

    class Config:
        from_attributes = True


class OrderStatusHistoryResponseSchema(BaseModel):
    order_id: int = Field(default=..., description="Order ID")
    history: list[OrderStatusResponseSchema] = Field(
        default=..., description="Status history"
    )
    total_duration_seconds: int | None = Field(
        default=None, description="Total duration of the status in seconds"
    )

    class Config:
        from_attributes = True
