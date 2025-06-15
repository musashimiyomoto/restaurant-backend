from db.models import Schedule
from repositories.base import BaseRepository


class ScheduleRepository(BaseRepository[Schedule]):
    def __init__(self):
        super().__init__(Schedule)
