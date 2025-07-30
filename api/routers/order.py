from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, order
from enums.order import OrderStatusEnum
from schemas import (
    ClientResponseSchema,
    OrderCreateSchema,
    OrderFilterSchema,
    OrderResponseSchema,
    OrderStatusHistoryResponseSchema,
    OrderStatusSchema,
)

router = APIRouter(prefix="/order", tags=["Order"])


@router.get(path="/list")
async def get_list(
    filters: Annotated[OrderFilterSchema, Query(description="Order filters")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> list[OrderResponseSchema]:
    return await usecase.get_orders(
        session=session, client_id=current_client.id, filters=filters
    )


@router.get(path="/{order_id}")
async def get_order_by_id(
    order_id: Annotated[int, Path(description="Order ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> OrderResponseSchema:
    return await usecase.get_order_by_id(
        session=session,
        order_id=order_id,
        client_id=current_client.id,
    )


@router.post(path="/create")
async def create(
    data: Annotated[OrderCreateSchema, Body(description="Order data for create")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> OrderResponseSchema:
    return await usecase.create_order(
        session=session,
        data=data,
        client_id=current_client.id,
        user_id=current_client.user_id,
    )


@router.patch(path="/{order_id}/status/{new_status}")
async def update_status(
    order_id: Annotated[int, Path(description="Order ID")],
    new_status: Annotated[OrderStatusEnum, Path(description="New status")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> OrderResponseSchema:
    return await usecase.update_order_status(
        session=session,
        order_id=order_id,
        new_status=new_status,
        current_client=current_client,
    )


@router.get(path="/{order_id}/status/transitions")
async def get_available_status_transitions(
    order_id: Annotated[int, Path(description="Order ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> list[OrderStatusSchema]:
    return [
        OrderStatusSchema(
            value=status.value, name=status.name, description=status.description
        )
        for status in await usecase.get_available_status_transitions(
            session=session,
            order_id=order_id,
            current_client=current_client,
        )
    ]


@router.get(path="/{order_id}/status/history")
async def get_order_status_history(
    order_id: Annotated[int, Path(description="Order ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[order.OrderUsecase, Depends(dependency=order.get_order_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> OrderStatusHistoryResponseSchema:
    return await usecase.get_order_status_history(
        session=session,
        order_id=order_id,
        current_client=current_client,
    )
