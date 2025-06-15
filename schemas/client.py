from datetime import datetime

from pydantic import BaseModel, Field


class ClientBaseSchema(BaseModel):
    email: str | None = Field(default=None, description="Email")
    telegram_id: int | None = Field(default=None, description="Telegram ID", gt=0)
    telegram_username: str | None = Field(default=None, description="Telegram username")

    first_name: str | None = Field(default=None, description="First name")
    last_name: str | None = Field(default=None, description="Last name")


class ClientCreateSchema(ClientBaseSchema):
    user_id: int = Field(default=..., description="User ID", gt=0)
    password: str = Field(default=..., description="Password")


class ClientResponseSchema(ClientBaseSchema):
    id: int = Field(default=..., description="ID", gt=0)
    user_id: int = Field(default=..., description="User ID", gt=0)

    created_at: datetime = Field(default=..., description="Created at")
    last_login: datetime | None = Field(default=None, description="Last login")

    is_active: bool = Field(default=True, description="Is active")

    class Config:
        from_attributes = True
