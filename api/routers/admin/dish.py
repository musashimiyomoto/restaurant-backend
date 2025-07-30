from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, dish
from schemas import DishFilterSchema, DishResponseSchema, admin

router = APIRouter(prefix="/dish", tags=["Admin | Dish"])


@router.get(path="/list")
async def get_list(
    filters: Annotated[DishFilterSchema, Query(description="Dish filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[dish.DishUsecase, Depends(dependency=dish.get_dish_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> list[DishResponseSchema]:
    return await usecase.get_dishes(
        session=session, user_id=current_user.id, category_id=filters.category_id
    )


@router.post(path="/create")
async def create(
    data: Annotated[admin.DishCreateSchema, Body(description="Dish data for create")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[dish.DishUsecase, Depends(dependency=dish.get_dish_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> DishResponseSchema:
    return await usecase.create_dish(
        session=session, data=data, user_id=current_user.id
    )


@router.put(path="/{dish_id}")
async def update(
    dish_id: Annotated[int, Path(description="Dish ID")],
    data: Annotated[admin.DishUpdateSchema, Body(description="Dish data for update")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[dish.DishUsecase, Depends(dependency=dish.get_dish_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> DishResponseSchema:
    return await usecase.update_dish(
        session=session, dish_id=dish_id, data=data, user_id=current_user.id
    )


@router.delete(path="/{dish_id}")
async def delete(
    dish_id: Annotated[int, Path(description="Dish ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[dish.DishUsecase, Depends(dependency=dish.get_dish_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> JSONResponse:
    await usecase.delete_dish(session=session, dish_id=dish_id, user_id=current_user.id)

    return JSONResponse(
        content={"message": "Dish deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
