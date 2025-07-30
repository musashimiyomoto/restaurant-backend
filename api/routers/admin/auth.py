from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db
from enums.role import UserRoleEnum
from schemas import TokenSchema, admin
from utils.category import generate_categories
from utils.delivery import generate_deliveries
from utils.schedule import generate_schedules

router = APIRouter(prefix="/auth", tags=["Admin | Auth"])


@router.post(path="/token")
async def login(
    data: Annotated[admin.LoginAdminSchema, Body(description="User data for login")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.UserAuthUsecase, Depends(dependency=auth.get_user_auth_usecase)
    ],
) -> TokenSchema:
    return await usecase.login(session=session, **data.model_dump())


@router.post(path="/register")
async def register(
    background_tasks: BackgroundTasks,
    data: Annotated[admin.UserCreateSchema, Body(description="User data for register")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.UserAuthUsecase, Depends(dependency=auth.get_user_auth_usecase)
    ],
) -> admin.UserResponseSchema:
    user = await usecase.register(session=session, data=data, role=UserRoleEnum.ADMIN)
    background_tasks.add_task(generate_categories, session=session, user_id=user.id)
    background_tasks.add_task(generate_deliveries, session=session, user_id=user.id)
    background_tasks.add_task(generate_schedules, session=session, user_id=user.id)
    return user


@router.post(path="/send/{email}/code")
async def send_email_code(
    email: Annotated[str, Path(description="Email for sending code")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.UserAuthUsecase, Depends(dependency=auth.get_user_auth_usecase)
    ],
) -> JSONResponse:
    await usecase.send_email_code(session=session, email=email)
    return JSONResponse(
        content={"message": "Email code sent successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.post(path="/verify/{email}/{code}")
async def verify_email(
    email: Annotated[str, Path(description="Email for verification")],
    code: Annotated[str, Path(description="Code for verification")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        auth.UserAuthUsecase, Depends(dependency=auth.get_user_auth_usecase)
    ],
) -> JSONResponse:
    await usecase.verify_email(session=session, email=email, code=code)
    return JSONResponse(
        content={"message": "Email verified successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
