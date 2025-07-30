from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, delivery
from schemas import ClientResponseSchema, DeliveryResponseSchema

router = APIRouter(prefix="/delivery", tags=["Delivery"])


@router.get(path="/list")
async def get_list(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        delivery.DeliveryUsecase, Depends(dependency=delivery.get_delivery_usecase)
    ],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> list[DeliveryResponseSchema]:
    return await usecase.get_deliveries(session=session, user_id=current_client.user_id)
