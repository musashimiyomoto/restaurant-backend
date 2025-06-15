from usecases.statistics import StatisticsUsecase


def get_statistics_usecase() -> StatisticsUsecase:
    """Get the statistics usecase.

    Returns:
        The statistics usecase.

    """
    return StatisticsUsecase()
