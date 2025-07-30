from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, dish
from schemas import ClientResponseSchema, DishFilterSchema, DishResponseSchema

router = APIRouter(prefix="/dish", tags=["Dish"])


@router.get(path="/list")
async def get_list(
    filters: Annotated[DishFilterSchema, Query(description="Dish filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[dish.DishUsecase, Depends(dependency=dish.get_dish_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> list[DishResponseSchema]:
    return await usecase.get_dishes(
        session=session, user_id=current_client.user_id, category_id=filters.category_id
    )
