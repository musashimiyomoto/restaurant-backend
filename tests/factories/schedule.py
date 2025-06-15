from datetime import time

import factory

from db.models.schedule import Schedule
from enums.date import DayEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class ScheduleFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Schedule

    user_id = factory.Sequence(lambda n: n + 1)
    day = factory.Iterator(DayEnum)
    start = factory.LazyAttribute(
        lambda obj: time(hour=fake.random_int(min=8, max=11), minute=0)
    )
    end = factory.LazyAttribute(
        lambda obj: time(hour=fake.random_int(min=18, max=23), minute=0)
    )
