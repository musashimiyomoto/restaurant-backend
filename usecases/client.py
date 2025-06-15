from sqlalchemy.ext.asyncio import AsyncSession

from repositories import ClientRepository
from schemas import ClientResponseSchema


class ClientUsecase:
    def __init__(self):
        self._client_repository = ClientRepository()

    async def get_clients(
        self, session: AsyncSession, user_id: int
    ) -> list[ClientResponseSchema]:
        """Get the clients.

        Args:
            session: The session.
            user_id: The user ID.

        Returns:
            The clients.

        """
        return list(
            map(
                ClientResponseSchema.model_validate,
                await self._client_repository.get_all(session=session, user_id=user_id),
            )
        )
