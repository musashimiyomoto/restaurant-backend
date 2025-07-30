from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, schedule
from enums.date import DayEnum
from schemas import ScheduleResponseSchema, admin

router = APIRouter(prefix="/schedule", tags=["Admin | Schedule"])


@router.get(path="")
async def get_list(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        schedule.ScheduleUsecase, Depends(dependency=schedule.get_schedule_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> list[ScheduleResponseSchema]:
    return await usecase.get_schedules(session=session, user_id=current_user.id)


@router.post(path="/create")
async def create(
    data: Annotated[
        admin.ScheduleCreateSchema, Body(description="Schedule data for create")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        schedule.ScheduleUsecase, Depends(dependency=schedule.get_schedule_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> ScheduleResponseSchema:
    return await usecase.create_schedule(
        session=session, data=data, user_id=current_user.id
    )


@router.put(path="/{day}")
async def update(
    day: Annotated[DayEnum, Path(description="Day")],
    data: Annotated[
        admin.ScheduleUpdateSchema, Body(description="Schedule data for update")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        schedule.ScheduleUsecase, Depends(dependency=schedule.get_schedule_usecase)
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> ScheduleResponseSchema:
    return await usecase.update_schedule(
        session=session, day=day, data=data, user_id=current_user.id
    )
