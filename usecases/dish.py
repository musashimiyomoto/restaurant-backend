from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import DishRepository
from schemas import DishResponseSchema, admin


class DishUsecase:
    def __init__(self):
        self._dish_repository = DishRepository()

    async def get_dishes(
        self, session: AsyncSession, user_id: int, category_id: int | None
    ) -> list[DishResponseSchema]:
        """Get the dishes.

        Args:
            session: The session.
            user_id: The user ID.
            category_id: The category ID.

        Returns:
            The dishes.

        """
        filters = (
            {"user_id": user_id, "category_id": category_id}
            if category_id
            else {"user_id": user_id}
        )

        return list(
            map(
                DishResponseSchema.model_validate,
                await self._dish_repository.get_all(session=session, **filters),
            )
        )

    async def create_dish(
        self, session: AsyncSession, data: admin.DishCreateSchema, user_id: int
    ) -> DishResponseSchema:
        """Create a dish.

        Args:
            session: The session.
            data: The data.
            user_id: The user ID.

        Returns:
            The dish.

        """
        return DishResponseSchema.model_validate(
            await self._dish_repository.create(
                session=session,
                data={**data.model_dump(exclude_none=True), "user_id": user_id},
            )
        )

    async def update_dish(
        self,
        session: AsyncSession,
        dish_id: int,
        data: admin.DishUpdateSchema,
        user_id: int,
    ) -> DishResponseSchema:
        """Update a dish.

        Args:
            session: The session.
            dish_id: The dish ID.
            data: The data.
            user_id: The user ID.

        Returns:
            The dish.

        """
        if not await self._dish_repository.get_by(
            session=session, user_id=user_id, id=dish_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found"
            )

        return DishResponseSchema.model_validate(
            await self._dish_repository.update_by(
                session=session, data=data.model_dump(exclude_none=True), id=dish_id
            )
        )

    async def delete_dish(
        self, session: AsyncSession, dish_id: int, user_id: int
    ) -> None:
        """Delete a dish.

        Args:
            session: The session.
            dish_id: The dish ID.
            user_id: The user ID.

        """
        if not await self._dish_repository.get_by(
            session=session, user_id=user_id, id=dish_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found"
            )

        await self._dish_repository.delete_by(session=session, id=dish_id)
