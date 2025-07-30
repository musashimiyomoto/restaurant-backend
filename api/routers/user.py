from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, user
from schemas import ClientResponseSchema, UserResponseSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get(path="")
async def get_user(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[user.UserUsecase, Depends(dependency=user.get_user_usecase)],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> UserResponseSchema:
    return await usecase.get_user(session=session, user_id=current_client.user_id)
