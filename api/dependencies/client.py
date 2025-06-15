from usecases.client import ClientUsecase


def get_client_usecase() -> ClientUsecase:
    """Get the client usecase.

    Returns:
        The client usecase.

    """
    return ClientUsecase()
