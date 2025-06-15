from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db
from schemas import ClientCreateSchema, ClientResponseSchema, LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(path="/token")
async def login(
    data: LoginSchema = Body(default=..., description="Client data for login"),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: auth.ClientAuthUsecase = Depends(dependency=auth.get_client_auth_usecase),
) -> TokenSchema:
    return await usecase.login(session=session, **data.model_dump())


@router.post(path="/register")
async def register(
    data: ClientCreateSchema = Body(
        default=..., description="Client data for register"
    ),
    session: AsyncSession = Depends(dependency=db.get_session),
    usecase: auth.ClientAuthUsecase = Depends(dependency=auth.get_client_auth_usecase),
) -> ClientResponseSchema:
    return await usecase.register(session=session, data=data)
