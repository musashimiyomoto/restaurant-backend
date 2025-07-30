from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, client, db
from schemas import ClientResponseSchema, admin

router = APIRouter(prefix="/client", tags=["Admin | Client"])


@router.get(path="/list")
async def get_list(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        client.ClientUsecase, Depends(dependency=client.get_client_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> list[ClientResponseSchema]:
    return await usecase.get_clients(session=session, user_id=current_user.id)
