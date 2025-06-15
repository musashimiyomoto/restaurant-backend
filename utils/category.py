from sqlalchemy.ext.asyncio import AsyncSession

from constants.category import DEFAULT_CATEGORIES
from repositories import CategoryRepository


async def generate_categories(session: AsyncSession, user_id: int) -> None:
    """Generate the categories in the database.

    Args:
        session: The session of the database.
        user_id: The id of the user.

    """
    category_repository = CategoryRepository()

    for category in DEFAULT_CATEGORIES:
        category_instance = await category_repository.create(
            session=session,
            data={
                "name": category["name"],
                "user_id": user_id,
                "is_type": False,
                "is_sub_type": False,
                "parent_id": None,
            },
        )

        for type in category["types"]:
            type_instance = await category_repository.create(
                session=session,
                data={
                    "name": type["name"],
                    "user_id": user_id,
                    "is_type": True,
                    "is_sub_type": False,
                    "parent_id": category_instance.id,
                },
            )

            for sub_type in type["sub_types"]:
                await category_repository.create(
                    session=session,
                    data={
                        "name": sub_type,
                        "user_id": user_id,
                        "is_type": False,
                        "is_sub_type": True,
                        "parent_id": type_instance.id,
                    },
                )
