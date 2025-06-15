from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from enums.role import UserRoleEnum
from repositories import UserRepository
from schemas import UserResponseSchema, admin


class UserUsecase:
    def __init__(self):
        self._user_repository = UserRepository()

    async def get_user(self, session: AsyncSession, user_id: int) -> UserResponseSchema:
        """Get a user.

        Args:
            session: The session.
            user_id: The user ID.

        Returns:
            The user.

        """
        user = await self._user_repository.get_by(session=session, id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return UserResponseSchema.model_validate(user)

    async def get_list(
        self, session: AsyncSession, parent_id: int, role: UserRoleEnum | None = None
    ) -> list[admin.UserResponseSchema]:
        """Get a list of users.

        Args:
            session: The session.
            parent_id: The parent ID.

        Returns:
            The list of users.

        """
        filters = (
            {"parent_id": parent_id, "role": role} if role else {"parent_id": parent_id}
        )
        return [
            admin.UserResponseSchema.model_validate(user)
            for user in await self._user_repository.get_all(session=session, **filters)
        ]
