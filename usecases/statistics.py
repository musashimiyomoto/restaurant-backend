from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from enums.redis import CachePrefixEnum
from repositories import StatisticsRepository
from schemas import admin
from utils.redis import generate_cache_name, get_cache, set_cache


class StatisticsUsecase:
    def __init__(self):
        self._statistics_repository = StatisticsRepository()

    async def get_statistics(
        self, session: AsyncSession, user_id: int, filters: admin.StatisticsFilterSchema
    ) -> admin.StatisticsResponseSchema:
        cache_name = generate_cache_name(
            prefix=CachePrefixEnum.STATISTICS.value.format(user_id=user_id),
            **filters.model_dump(exclude_none=True),
        )

        cached_data = await get_cache(name=cache_name)
        if cached_data:
            return admin.StatisticsResponseSchema.model_validate(cached_data)

        start_date = datetime.combine(filters.start_date, datetime.min.time())
        end_date = datetime.combine(filters.end_date, datetime.max.time())

        periods = [
            admin.StatisticsPeriodSchema.model_validate(period)
            for period in await self._statistics_repository.get_statistics(
                session=session,
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                interval=filters.interval,
            )
        ]

        statistics = admin.StatisticsResponseSchema(
            date_min=filters.start_date.isoformat(),
            date_max=filters.end_date.isoformat(),
            totals=admin.StatisticsTotalsSchema(
                orders_count=sum(period.orders_count for period in periods),
                new_clients_count=sum(period.new_clients_count for period in periods),
                avg_order_price=(
                    sum(
                        period.avg_order_price * period.orders_count
                        for period in periods
                    )
                    / sum(period.orders_count for period in periods)
                    if sum(period.orders_count for period in periods) > 0
                    else 0.0
                ),
                avg_order_time=(
                    sum(
                        period.avg_order_time * period.orders_count
                        for period in periods
                    )
                    / sum(period.orders_count for period in periods)
                    if sum(period.orders_count for period in periods) > 0
                    else 0.0
                ),
            ),
            periods=periods,
            interval=filters.interval,
        )

        await set_cache(name=cache_name, value=statistics.model_dump(exclude_none=True))

        return statistics
