from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, schedule
from schemas import ClientResponseSchema, ScheduleResponseSchema

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.get(path="")
async def get_list(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        schedule.ScheduleUsecase, Depends(dependency=schedule.get_schedule_usecase)
    ],
    current_client: Annotated[
        ClientResponseSchema, Depends(dependency=auth.get_current_client)
    ],
) -> list[ScheduleResponseSchema]:
    return await usecase.get_schedules(session=session, user_id=current_client.user_id)
