from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, category, db
from schemas import CategoryFilterSchema, CategoryResponseSchema, ClientResponseSchema

router = APIRouter(prefix="/category", tags=["Category"])


@router.get(path="/list")
async def get_list(
    filters: Annotated[CategoryFilterSchema, Query(description="Category filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        category.CategoryUsecase, Depends(dependency=category.get_category_usecase)
    ],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> list[CategoryResponseSchema]:
    return await usecase.get_categories(
        session=session, user_id=current_client.user_id, filters=filters
    )
