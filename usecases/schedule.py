from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from enums.date import DayEnum
from repositories import ScheduleRepository
from schemas import ScheduleResponseSchema, admin


class ScheduleUsecase:
    def __init__(self):
        self._schedule_repository = ScheduleRepository()

    async def get_schedules(
        self, session: AsyncSession, user_id: int
    ) -> list[ScheduleResponseSchema]:
        return list(
            map(
                ScheduleResponseSchema.model_validate,
                await self._schedule_repository.get_all(
                    session=session, user_id=user_id
                ),
            )
        )

    async def create_schedule(
        self, session: AsyncSession, data: admin.ScheduleCreateSchema, user_id: int
    ) -> ScheduleResponseSchema:
        return ScheduleResponseSchema.model_validate(
            await self._schedule_repository.create(
                session=session,
                data={**data.model_dump(exclude_none=True), "user_id": user_id},
            )
        )

    async def update_schedule(
        self,
        session: AsyncSession,
        day: DayEnum,
        data: admin.ScheduleUpdateSchema,
        user_id: int,
    ) -> ScheduleResponseSchema:
        if not await self._schedule_repository.get_by(
            session=session, user_id=user_id, day=day
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found"
            )

        return ScheduleResponseSchema.model_validate(
            await self._schedule_repository.update_by(
                session=session,
                data=data.model_dump(exclude_none=True),
                user_id=user_id,
                day=day,
            )
        )
