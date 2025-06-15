from pydantic import BaseModel, Field


class CategoryCreateSchema(BaseModel):
    name: str = Field(default=..., description="Name")

    parent_id: int | None = Field(default=None, description="Parent ID", gt=0)

    is_type: bool = Field(default=False, description="Is Type")
    is_sub_type: bool = Field(default=False, description="Is Subtype")


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="Name")

    parent_id: int | None = Field(default=None, description="Parent ID", gt=0)

    is_type: bool | None = Field(default=None, description="Is Type")
    is_sub_type: bool | None = Field(default=None, description="Is Subtype")
