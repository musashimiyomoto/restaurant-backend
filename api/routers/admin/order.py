from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, order
from enums.order import OrderStatusEnum
from enums.role import UserRoleEnum
from schemas import (
    OrderResponseSchema,
    OrderStatusHistoryResponseSchema,
    OrderStatusSchema,
    admin,
)

router = APIRouter(prefix="/order", tags=["Admin | Order"])


@router.get(path="/list")
async def get_list(
    filters: Annotated[admin.OrderFilterSchema, Query(description="Order filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=False)),
    ],
) -> list[OrderResponseSchema]:
    return await usecase.get_orders(
        session=session,
        user_id=current_user.id,
        filters=filters,
        is_admin=current_user.role == UserRoleEnum.ADMIN,
    )


@router.get(path="/{order_id}")
async def get_order_by_id(
    order_id: Annotated[int, Path(description="Order ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=False)),
    ],
) -> OrderResponseSchema:
    return await usecase.get_order_by_id(
        session=session,
        order_id=order_id,
        user_id=current_user.id,
        is_admin=current_user.role == UserRoleEnum.ADMIN,
    )


@router.patch(path="/{order_id}/status/{new_status}")
async def update_status(
    order_id: Annotated[int, Path(description="Order ID")],
    new_status: Annotated[OrderStatusEnum, Path(description="New status")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=False)),
    ],
) -> OrderResponseSchema:
    return await usecase.update_order_status(
        session=session,
        order_id=order_id,
        new_status=new_status,
        current_user=current_user,
    )


@router.get(path="/{order_id}/status/transitions")
async def get_available_status_transitions(
    order_id: Annotated[int, Path(description="Order ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=False)),
    ],
) -> list[OrderStatusSchema]:
    return [
        OrderStatusSchema(
            value=status.value, name=status.name, description=status.description
        )
        for status in await usecase.get_available_status_transitions(
            session=session,
            order_id=order_id,
            current_user=current_user,
        )
    ]


@router.get(path="/{order_id}/status/history")
async def get_order_status_history(
    order_id: Annotated[int, Path(description="Order ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=False)),
    ],
) -> OrderStatusHistoryResponseSchema:
    return await usecase.get_order_status_history(
        session=session,
        order_id=order_id,
        current_user=current_user,
    )
