from pydantic import BaseModel, Field


class LoginAdminSchema(BaseModel):
    email: str = Field(default=..., description="Email of the user")

    password: str = Field(default=..., description="Password of the user")
