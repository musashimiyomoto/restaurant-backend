from pydantic import BaseModel, Field


class CategoryFilterSchema(BaseModel):
    parent_id: int | None = Field(default=None, description="Parent ID", gt=0)

    is_type: bool = Field(default=False, description="Is type")
    is_sub_type: bool = Field(default=False, description="Is sub type")


class CategoryResponseSchema(BaseModel):
    id: int = Field(default=..., description="ID", gt=0)

    parent_id: int | None = Field(default=None, description="Parent ID", gt=0)

    name: str = Field(default=..., description="Name")
    is_type: bool = Field(default=False, description="Is type")
    is_sub_type: bool = Field(default=False, description="Is sub type")

    class Config:
        from_attributes = True
