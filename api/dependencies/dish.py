from usecases.dish import DishUsecase


def get_dish_usecase() -> DishUsecase:
    """Get the dish usecase.

    Returns:
        The dish usecase.

    """
    return DishUsecase()
