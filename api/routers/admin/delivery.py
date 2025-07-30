from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, delivery
from schemas import DeliveryResponseSchema, admin

router = APIRouter(prefix="/delivery", tags=["Admin | Delivery"])


@router.get(path="/list")
async def get_list(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        delivery.DeliveryUsecase, Depends(dependency=delivery.get_delivery_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> list[DeliveryResponseSchema]:
    return await usecase.get_deliveries(session=session, user_id=current_user.id)


@router.post(path="/create")
async def create(
    data: Annotated[
        admin.DeliveryCreateSchema, Body(description="Delivery data for create")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        delivery.DeliveryUsecase, Depends(dependency=delivery.get_delivery_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> DeliveryResponseSchema:
    return await usecase.create_delivery(
        session=session, user_id=current_user.id, data=data
    )


@router.put(path="/{delivery_id}")
async def update(
    delivery_id: Annotated[int, Path(description="Delivery ID")],
    data: Annotated[
        admin.DeliveryUpdateSchema, Body(description="Delivery data for update")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        delivery.DeliveryUsecase, Depends(dependency=delivery.get_delivery_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> DeliveryResponseSchema:
    return await usecase.update_delivery(
        session=session, user_id=current_user.id, delivery_id=delivery_id, data=data
    )


@router.delete(path="/{delivery_id}")
async def delete(
    delivery_id: Annotated[int, Path(description="Delivery ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        delivery.DeliveryUsecase, Depends(dependency=delivery.get_delivery_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> JSONResponse:
    await usecase.delete_delivery(
        session=session, user_id=current_user.id, delivery_id=delivery_id
    )

    return JSONResponse(
        content={"message": "Delivery deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
