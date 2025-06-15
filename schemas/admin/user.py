from datetime import datetime

from pydantic import BaseModel, Field

from enums.role import UserRoleEnum


class UserBaseSchema(BaseModel):
    name: str = Field(default=..., description="Name of the user")
    email: str = Field(default=..., description="Email of the user")
    telegram_id: int | None = Field(default=None, description="Telegram ID of the user")
    telegram_username: str | None = Field(
        default=None, description="Telegram username of the user"
    )
    photo_url: str | None = Field(default=None, description="Photo URL of the user")
    parent_id: int | None = Field(default=None, description="Parent ID of the user")


class UserCreateSchema(UserBaseSchema):
    password: str = Field(default=..., description="Password of the user")


class UserResponseSchema(UserBaseSchema):
    id: int = Field(default=..., description="ID of the user", gt=0)

    is_active: bool = Field(default=..., description="Is the user active")

    role: UserRoleEnum = Field(default=..., description="Role of the user")

    created_at: datetime = Field(default=..., description="Created at")

    class Config:
        from_attributes = True


class UserFilterSchema(BaseModel):
    role: UserRoleEnum | None = Field(default=None, description="Role of the user")
