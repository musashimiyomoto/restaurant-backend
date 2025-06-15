from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, user
from schemas import ClientResponseSchema, UserResponseSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get(path="")
async def get_user(
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: user.UserUsecase = Depends(dependency=user.get_user_usecase),
    current_client: ClientResponseSchema = Depends(dependency=auth.get_current_client),
) -> UserResponseSchema:
    return await usecase.get_user(session=session, user_id=current_client.user_id)
