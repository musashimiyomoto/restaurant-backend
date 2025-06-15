from pydantic import BaseModel, Field


class UserResponseSchema(BaseModel):
    id: int = Field(default=..., description="User ID", gt=0)

    name: str = Field(default=..., description="User name")
    photo_url: str | None = Field(default=None, description="User photo URL")

    class Config:
        from_attributes = True
