from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import DeliveryRepository
from schemas import DeliveryResponseSchema, admin


class DeliveryUsecase:
    def __init__(self):
        self._delivery_repository = DeliveryRepository()

    async def get_deliveries(
        self, session: AsyncSession, user_id: int
    ) -> list[DeliveryResponseSchema]:
        """Get all deliveries for a user.

        Args:
            session: The session.
            user_id: The user ID.

        Returns:
            The deliveries.

        """
        return list(
            map(
                DeliveryResponseSchema.model_validate,
                await self._delivery_repository.get_all(
                    session=session, user_id=user_id
                ),
            )
        )

    async def update_delivery(
        self,
        session: AsyncSession,
        user_id: int,
        delivery_id: int,
        data: admin.DeliveryUpdateSchema,
    ) -> DeliveryResponseSchema | None:
        """Update a delivery.

        Args:
            session: The session.
            user_id: The user ID.
            delivery_id: The delivery ID.
            data: The data.

        Returns:
            The delivery.

        """
        if not await self._delivery_repository.get_by(
            session=session, user_id=user_id, id=delivery_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found"
            )

        return DeliveryResponseSchema.model_validate(
            await self._delivery_repository.update_by(
                session=session, data=data.model_dump(exclude_none=True), id=delivery_id
            )
        )

    async def create_delivery(
        self, session: AsyncSession, user_id: int, data: admin.DeliveryCreateSchema
    ) -> DeliveryResponseSchema:
        """Create a delivery.

        Args:
            session: The session.
            user_id: The user ID.
            data: The data.

        Returns:
            The delivery.

        """
        return DeliveryResponseSchema.model_validate(
            await self._delivery_repository.create(
                session=session,
                data={**data.model_dump(exclude_none=True), "user_id": user_id},
            )
        )

    async def delete_delivery(
        self, session: AsyncSession, user_id: int, delivery_id: int
    ) -> None:
        """Delete a delivery.

        Args:
            session: The session.
            user_id: The user ID.
            delivery_id: The delivery ID.

        """
        if not await self._delivery_repository.get_by(
            session=session, user_id=user_id, id=delivery_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found"
            )

        await self._delivery_repository.delete_by(session=session, id=delivery_id)
