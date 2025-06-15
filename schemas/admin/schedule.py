from datetime import time

from pydantic import BaseModel, Field

from enums.date import DayEnum


class ScheduleCreateSchema(BaseModel):
    day: DayEnum = Field(default=..., description="Day")
    start: time = Field(default=..., description="Start")
    end: time = Field(default=..., description="End")


class ScheduleUpdateSchema(BaseModel):
    start: time | None = Field(default=None, description="Start")
    end: time | None = Field(default=None, description="End")
