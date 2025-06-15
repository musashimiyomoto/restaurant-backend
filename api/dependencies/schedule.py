from usecases.schedule import ScheduleUsecase


def get_schedule_usecase() -> ScheduleUsecase:
    """Get the schedule usecase.

    Returns:
        The schedule usecase.

    """
    return ScheduleUsecase()
