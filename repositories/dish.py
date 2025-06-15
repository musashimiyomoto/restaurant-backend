from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Category, Dish
from repositories.base import BaseRepository


class DishRepository(BaseRepository[Dish]):
    def __init__(self):
        super().__init__(Dish)

    async def _get_category_ids(
        self, session: AsyncSession, category_id: int
    ) -> list[int]:
        """Get the category ids.

        Args:
            session: The async session.
            category_id: The id of the category.

        Returns:
            The list of category ids.

        """
        category = await session.execute(
            statement=select(Category).filter_by(id=category_id)
        )
        category = category.scalar_one_or_none()

        if not category:
            return []

        if not category.is_type and not category.is_sub_type:
            type_category_ids = await session.execute(
                statement=select(Category.id).filter_by(parent_id=category_id)
            )
            type_category_ids = type_category_ids.scalars().all()

            sub_type_categories_ids = await session.execute(
                statement=select(Category.id).where(
                    Category.parent_id.in_(type_category_ids)
                )
            )

            return (
                [category.id]
                + type_category_ids
                + sub_type_categories_ids.scalars().all()
            )
        elif not category.is_sub_type:
            sub_type_category_ids = await session.execute(
                statement=select(Category.id).filter_by(parent_id=category_id)
            )

            return [category.id] + sub_type_category_ids.scalars().all()
        else:
            return [category.id]

    async def get_all(self, session: AsyncSession, **filters) -> list[Dish]:
        """Get all dishes.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            The list of dishes.

        """
        statement = select(self.model)

        dish_id, user_id, category_id = (
            filters.get("id"),
            filters.get("user_id"),
            filters.get("category_id"),
        )

        if dish_id:
            statement = statement.filter_by(id=dish_id)
        if user_id:
            statement = statement.filter_by(user_id=user_id)
        if category_id:
            statement = statement.where(
                self.model.category_id.in_(
                    await self._get_category_ids(
                        session=session, category_id=category_id
                    )
                )
            )

        result = await session.execute(statement=statement)
        return result.scalars().all()
