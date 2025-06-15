from pydantic import BaseModel, Field


class ImageResponseSchema(BaseModel):
    url: str = Field(default=..., description="The URL of the image")
