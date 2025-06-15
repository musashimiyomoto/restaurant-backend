from usecases.order import OrderUsecase


def get_order_usecase() -> OrderUsecase:
    """Get the order usecase.

    Returns:
        The order usecase.

    """
    return OrderUsecase()
