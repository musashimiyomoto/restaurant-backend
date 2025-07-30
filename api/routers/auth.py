from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db
from schemas import ClientCreateSchema, ClientResponseSchema, LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(path="/token")
async def login(
    data: Annotated[LoginSchema, Body(description="Client data for login")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.ClientAuthUsecase, Depends(dependency=auth.get_client_auth_usecase)
    ],
) -> TokenSchema:
    return await usecase.login(session=session, **data.model_dump())


@router.post(path="/register")
async def register(
    data: Annotated[ClientCreateSchema, Body(description="Client data for register")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.ClientAuthUsecase, Depends(dependency=auth.get_client_auth_usecase)
    ],
) -> ClientResponseSchema:
    return await usecase.register(session=session, data=data)
