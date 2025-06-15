from datetime import time

from pydantic import BaseModel, Field

from enums.date import DayEnum


class ScheduleResponseSchema(BaseModel):
    id: int = Field(default=..., description="ID", gt=0)

    day: DayEnum = Field(default=..., description="Day")
    start: time = Field(default=..., description="Start")
    end: time = Field(default=..., description="End")

    class Config:
        from_attributes = True
