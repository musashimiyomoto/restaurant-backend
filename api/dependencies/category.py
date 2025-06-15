from usecases.category import CategoryUsecase


def get_category_usecase() -> CategoryUsecase:
    """Get the category usecase.

    Returns:
        The category usecase.

    """
    return CategoryUsecase()
