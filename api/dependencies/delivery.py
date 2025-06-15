from usecases import DeliveryUsecase


def get_delivery_usecase() -> DeliveryUsecase:
    """Get the delivery usecase.

    Returns:
        The delivery usecase.

    """
    return DeliveryUsecase()
