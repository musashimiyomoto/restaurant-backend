from datetime import time

from factory.declarations import Iterator, LazyAttribute, Sequence

from db.models.schedule import Schedule
from enums.date import DayEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class ScheduleFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Schedule

    user_id = Sequence(lambda n: n + 1)
    day = Iterator(DayEnum)
    start = LazyAttribute(
        lambda obj: time(hour=fake.random_int(min=8, max=11), minute=0)
    )
    end = LazyAttribute(
        lambda obj: time(hour=fake.random_int(min=18, max=23), minute=0)
    )
