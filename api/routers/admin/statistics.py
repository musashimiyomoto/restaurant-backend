from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, statistics
from schemas import admin

router = APIRouter(prefix="/statistics", tags=["Admin | Statistics"])


@router.get(path="")
async def get_list(
    filters: Annotated[
        admin.StatisticsFilterSchema, Query(description="Statistics filters")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        statistics.StatisticsUsecase,
        Depends(dependency=statistics.get_statistics_usecase),
    ],
    current_user: Annotated[
        admin.UserResponseSchema,
        Depends(dependency=auth.get_current_user(is_validate_admin=True)),
    ],
) -> admin.StatisticsResponseSchema:
    return await usecase.get_statistics(
        session=session, user_id=current_user.id, filters=filters
    )
