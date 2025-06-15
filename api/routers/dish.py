from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, dish
from schemas import ClientResponseSchema, DishFilterSchema, DishResponseSchema

router = APIRouter(prefix="/dish", tags=["Dish"])


@router.get(path="/list")
async def get_list(
    filters: DishFilterSchema = Query(default=..., description="Dish filters"),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: dish.DishUsecase = Depends(dependency=dish.get_dish_usecase),
    current_client: ClientResponseSchema = Depends(dependency=auth.get_current_client),
) -> list[DishResponseSchema]:
    return await usecase.get_dishes(
        session=session, user_id=current_client.user_id, category_id=filters.category_id
    )
