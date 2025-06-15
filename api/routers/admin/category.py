from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, category, db
from schemas import CategoryFilterSchema, CategoryResponseSchema, admin

router = APIRouter(prefix="/category", tags=["Admin | Category"])


@router.get(path="/list")
async def get_list(
    filters: CategoryFilterSchema = Query(default=..., description="Category filters"),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: category.CategoryUsecase = Depends(
        dependency=category.get_category_usecase
    ),
    current_user: admin.UserResponseSchema = Depends(
        dependency=auth.get_current_user(is_validate_admin=True)
    ),
) -> list[CategoryResponseSchema]:
    return await usecase.get_categories(
        session=session, user_id=current_user.id, filters=filters
    )


@router.post(path="/create")
async def create(
    data: admin.CategoryCreateSchema = Body(
        default=..., description="Category data for create"
    ),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: category.CategoryUsecase = Depends(
        dependency=category.get_category_usecase
    ),
    current_user: admin.UserResponseSchema = Depends(
        dependency=auth.get_current_user(is_validate_admin=True)
    ),
) -> CategoryResponseSchema:
    return await usecase.create_category(
        session=session, data=data, user_id=current_user.id
    )


@router.put(path="/{category_id}")
async def update(
    category_id: int = Path(default=..., description="Category ID"),
    data: admin.CategoryUpdateSchema = Body(
        default=..., description="Category data for update"
    ),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: category.CategoryUsecase = Depends(
        dependency=category.get_category_usecase
    ),
    current_user: admin.UserResponseSchema = Depends(
        dependency=auth.get_current_user(is_validate_admin=True)
    ),
) -> CategoryResponseSchema:
    return await usecase.update_category(
        session=session, category_id=category_id, data=data, user_id=current_user.id
    )


@router.delete(path="/{category_id}")
async def delete(
    category_id: int = Path(default=..., description="Category ID"),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: category.CategoryUsecase = Depends(
        dependency=category.get_category_usecase
    ),
    current_user: admin.UserResponseSchema = Depends(
        dependency=auth.get_current_user(is_validate_admin=True)
    ),
) -> JSONResponse:
    await usecase.delete_category(
        session=session, category_id=category_id, user_id=current_user.id
    )

    return JSONResponse(
        content={"message": "Category deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
