from sqlalchemy.ext.asyncio import AsyncSession

from constants.schedule import DEFAULT_SCHEDULES
from repositories import ScheduleRepository


async def generate_schedules(session: AsyncSession, user_id: int) -> None:
    """Generate the schedules in the database.

    Args:
        session: The session of the database.
        user_id: The id of the user.

    """
    schedule_repository = ScheduleRepository()

    for schedule in DEFAULT_SCHEDULES:
        await schedule_repository.create(
            session=session, data={**schedule, "user_id": user_id}
        )
