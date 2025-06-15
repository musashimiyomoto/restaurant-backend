from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db
from enums.role import UserRoleEnum
from schemas import ClientResponseSchema, UserResponseSchema
from usecases.auth import ClientAuthUsecase, UserAuthUsecase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


async def get_current_client(
    token: str = Depends(dependency=oauth2_scheme),
    session: AsyncSession = Depends(dependency=db.get_session),
) -> ClientResponseSchema:
    """Get the current client.

    Dependencies:
        token: The token.
        session: The session.

    Returns:
        The current client.

    """
    return await ClientAuthUsecase().get_current(token=token, session=session)


def get_current_user(
    is_validate_admin: bool,
) -> Callable[[str, AsyncSession], UserResponseSchema]:
    """Get the current user.

    Args:
        is_validate_admin: Whether to validate the admin.

    Returns:
        The current user.

    """

    async def _dependency(
        token: str = Depends(dependency=oauth2_scheme),
        session: AsyncSession = Depends(dependency=db.get_session),
    ) -> UserResponseSchema:
        user = await UserAuthUsecase().get_current(token=token, session=session)

        if is_validate_admin and user.role != UserRoleEnum.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        return user

    return _dependency


def get_client_auth_usecase() -> ClientAuthUsecase:
    """Get the client auth usecase.

    Returns:
        The client auth usecase.

    """
    return ClientAuthUsecase()


def get_user_auth_usecase() -> UserAuthUsecase:
    """Get the user auth usecase.

    Returns:
        The user auth usecase.

    """
    return UserAuthUsecase()
