from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import CategoryRepository
from schemas import CategoryFilterSchema, CategoryResponseSchema, admin


class CategoryUsecase:
    def __init__(self):
        self._category_repository = CategoryRepository()

    async def get_categories(
        self, session: AsyncSession, user_id: int, filters: CategoryFilterSchema
    ) -> list[CategoryResponseSchema]:
        """Get the categories.

        Args:
            session: The session.
            user_id: The user ID.
            filters: The filters.

        Returns:
            The categories.

        """
        return [
            CategoryResponseSchema.model_validate(category)
            for category in await self._category_repository.get_all(
                session=session,
                user_id=user_id,
                **filters.model_dump(exclude_none=True),
            )
        ]

    async def create_category(
        self, session: AsyncSession, data: admin.CategoryCreateSchema, user_id: int
    ) -> CategoryResponseSchema:
        """Create a category.

        Args:
            session: The session.
            data: The data.
            user_id: The user ID.

        Returns:
            The category.

        """
        return CategoryResponseSchema.model_validate(
            await self._category_repository.create(
                session=session,
                data={**data.model_dump(exclude_none=True), "user_id": user_id},
            )
        )

    async def update_category(
        self,
        session: AsyncSession,
        category_id: int,
        data: admin.CategoryUpdateSchema,
        user_id: int,
    ) -> CategoryResponseSchema:
        """Update a category.

        Args:
            session: The session.
            category_id: The category ID.
            data: The data.
            user_id: The user ID.

        Returns:
            The category.

        """
        if not await self._category_repository.get_by(
            session=session, user_id=user_id, id=category_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        return CategoryResponseSchema.model_validate(
            await self._category_repository.update_by(
                session=session,
                data=data.model_dump(exclude_none=True),
                id=category_id,
            )
        )

    async def delete_category(
        self, session: AsyncSession, category_id: int, user_id: int
    ) -> None:
        """Delete a category.

        Args:
            session: The session.
            category_id: The category ID.
            user_id: The user ID.

        """
        if not await self._category_repository.get_by(
            session=session, user_id=user_id, id=category_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        await self._category_repository.delete_by(session=session, id=category_id)
