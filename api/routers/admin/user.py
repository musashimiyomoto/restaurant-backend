from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, user
from enums.role import UserRoleEnum
from schemas import admin

router = APIRouter(prefix="/user", tags=["Admin | User"])


@router.get(path="/me")
async def get_me(
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=False)),
    ],
) -> admin.UserResponseSchema:
    return current_user


@router.get(path="/list")
async def get_list(
    filters: Annotated[admin.UserFilterSchema, Query(description="User filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[user.UserUsecase, Depends(dependency=user.get_user_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> list[admin.UserResponseSchema]:
    return await usecase.get_list(
        session=session, parent_id=current_user.id, role=filters.role
    )


@router.post(path="/create/{role}")
async def create(
    role: Annotated[UserRoleEnum, Path(description="The role of the user")],
    data: Annotated[admin.UserCreateSchema, Body(description="User data for create")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.UserAuthUsecase, Depends(dependency=auth.get_user_auth_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> admin.UserResponseSchema:
    return await usecase.register(
        session=session,
        data=data,
        role=role,
        parent_id=current_user.id,
        is_active=True,
    )
