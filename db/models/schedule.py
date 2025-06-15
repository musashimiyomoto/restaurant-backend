from datetime import time

from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from enums.date import DayEnum


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Schedule ID"
    )

    user_id: Mapped[int] = mapped_column(index=True, comment="User ID")

    day: Mapped[DayEnum] = mapped_column(comment="Day")
    start: Mapped[time] = mapped_column(comment="Start time")
    end: Mapped[time] = mapped_column(comment="End time")
