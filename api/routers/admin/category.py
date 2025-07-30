from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, category, db
from schemas import CategoryFilterSchema, CategoryResponseSchema, admin

router = APIRouter(prefix="/category", tags=["Admin | Category"])


@router.get(path="/list")
async def get_list(
    filters: Annotated[CategoryFilterSchema, Query(description="Category filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        category.CategoryUsecase, Depends(dependency=category.get_category_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> list[CategoryResponseSchema]:
    return await usecase.get_categories(
        session=session, user_id=current_user.id, filters=filters
    )


@router.post(path="/create")
async def create(
    data: Annotated[
        admin.CategoryCreateSchema, Body(description="Category data for create")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        category.CategoryUsecase, Depends(dependency=category.get_category_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> CategoryResponseSchema:
    return await usecase.create_category(
        session=session, data=data, user_id=current_user.id
    )


@router.put(path="/{category_id}")
async def update(
    category_id: Annotated[int, Path(description="Category ID")],
    data: Annotated[
        admin.CategoryUpdateSchema, Body(description="Category data for update")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        category.CategoryUsecase, Depends(dependency=category.get_category_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> CategoryResponseSchema:
    return await usecase.update_category(
        session=session, category_id=category_id, data=data, user_id=current_user.id
    )


@router.delete(path="/{category_id}")
async def delete(
    category_id: Annotated[int, Path(description="Category ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        category.CategoryUsecase, Depends(dependency=category.get_category_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> JSONResponse:
    await usecase.delete_category(
        session=session, category_id=category_id, user_id=current_user.id
    )

    return JSONResponse(
        content={"message": "Category deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
