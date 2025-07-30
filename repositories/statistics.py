from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func, join, select
from sqlalchemy.ext.asyncio import AsyncSession

from constants.datetime import DATE_FORMAT, DECEMBER_MONTH
from db.models import Client, Order, OrderStatus
from enums.order import OrderStatusEnum
from enums.statistics import StatisticsIntervalEnum


class StatisticsRepository:
    def __init__(self):
        pass

    def _truncate_date(
        self, date: datetime, interval_type: StatisticsIntervalEnum
    ) -> datetime:
        if interval_type == StatisticsIntervalEnum.DAILY:
            return date.replace(hour=0, minute=0, second=0, microsecond=0)
        if interval_type == StatisticsIntervalEnum.WEEKLY:
            return (date - timedelta(days=date.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        if interval_type == StatisticsIntervalEnum.MONTHLY:
            return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return None

    def _get_next_date(
        self, current_date: datetime, interval: StatisticsIntervalEnum
    ) -> datetime:
        """Get the next date based on the interval type.

        Args:
            current_date: The current date.
            interval: The interval.

        Returns:
            The next date.

        """
        if interval == StatisticsIntervalEnum.DAILY:
            return current_date + timedelta(days=1)
        if interval == StatisticsIntervalEnum.WEEKLY:
            return current_date + timedelta(weeks=1)
        if interval == StatisticsIntervalEnum.MONTHLY:
            if current_date.month == DECEMBER_MONTH:
                return datetime(current_date.year + 1, 1, 1)
            return datetime(current_date.year, current_date.month + 1, 1)
        return None

    async def _get_orders_count(
        self,
        session: AsyncSession,
        user_id: int,
        current_date: datetime,
        next_date: datetime,
    ) -> int:
        """Get the count of orders for the given period.

        Args:
            session: The async session.
            user_id: The id of the user.
            current_date: The current date.
            next_date: The next date.

        Returns:
            The count of orders.

        """
        result = await session.execute(
            statement=select(func.count(Order.id)).where(
                Order.user_id == user_id,
                Order.created_at >= current_date,
                Order.created_at < next_date,
            )
        )
        return result.scalar() or 0

    async def _get_clients_count(
        self,
        session: AsyncSession,
        user_id: int,
        current_date: datetime,
        next_date: datetime,
    ) -> int:
        """Get the count of new clients for the given period.

        Args:
            session: The async session.
            user_id: The id of the user.
            current_date: The current date.
            next_date: The next date.

        Returns:
            The count of new clients.

        """
        result = await session.execute(
            statement=select(func.count(Client.id)).where(
                Client.user_id == user_id,
                Client.created_at >= current_date,
                Client.created_at < next_date,
            )
        )
        return result.scalar() or 0

    async def _get_avg_order_price(
        self,
        session: AsyncSession,
        user_id: int,
        current_date: datetime,
        next_date: datetime,
    ) -> float:
        """Get the average order price for the given period.

        Args:
            session: The async session.
            user_id: The id of the user.
            current_date: The current date.
            next_date: The next date.

        Returns:
            The average order price.

        """
        result = await session.execute(
            statement=select(func.avg(Order.price)).where(
                Order.user_id == user_id,
                Order.created_at >= current_date,
                Order.created_at < next_date,
            )
        )
        return float(result.scalar() or 0.0)

    async def _get_avg_order_time(
        self,
        session: AsyncSession,
        user_id: int,
        current_date: datetime,
        next_date: datetime,
    ) -> float:
        """Get the average order execution time for the given period.

        Args:
            session: The async session.
            user_id: The id of the user.
            current_date: The current date.
            next_date: The next date.

        Returns:
            The average order time.

        """
        start_times_subquery = (
            select(
                OrderStatus.order_id,
                OrderStatus.start_date.label("order_start_time"),
            )
            .where(OrderStatus.status == OrderStatusEnum.CLIENT_OPENED)
            .subquery()
        )

        end_times_subquery = (
            select(OrderStatus.order_id, OrderStatus.end_date.label("order_end_time"))
            .where(
                OrderStatus.status.in_(
                    [
                        OrderStatusEnum.DELIVERED,
                        OrderStatusEnum.RECEIVED,
                        OrderStatusEnum.CONSUMED,
                        OrderStatusEnum.RATED,
                    ]
                ),
                OrderStatus.end_date.is_not(None),
            )
            .subquery()
        )

        execution_times_subquery = (
            select(
                func.extract(
                    "epoch",
                    end_times_subquery.c.order_end_time
                    - start_times_subquery.c.order_start_time,
                ).label("execution_time_seconds")
            )
            .select_from(
                join(
                    join(
                        Order,
                        start_times_subquery,
                        Order.id == start_times_subquery.c.order_id,
                    ),
                    end_times_subquery,
                    Order.id == end_times_subquery.c.order_id,
                )
            )
            .where(
                Order.user_id == user_id,
                Order.created_at >= current_date,
                Order.created_at < next_date,
            )
            .subquery()
        )

        result = await session.execute(
            select(func.avg(execution_times_subquery.c.execution_time_seconds))
        )

        return float(result.scalar() or 0.0)

    async def get_statistics(
        self,
        session: AsyncSession,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        interval: StatisticsIntervalEnum,
    ) -> list[dict[str, Any]]:
        """Get the statistics.

        Args:
            session: The async session.
            user_id: The id of the user.
            start_date: The start date.
            end_date: The end date.
            interval: The interval.

        Returns:
            The statistics.

        """
        statistics = []

        current_date = self._truncate_date(date=start_date, interval_type=interval)
        end_date_truncated = self._truncate_date(date=end_date, interval_type=interval)

        while current_date <= end_date_truncated:
            next_date = self._get_next_date(
                current_date=current_date, interval=interval
            )

            statistics.append(
                {
                    "date": current_date.strftime(DATE_FORMAT),
                    "orders_count": await self._get_orders_count(
                        session=session,
                        user_id=user_id,
                        current_date=current_date,
                        next_date=next_date,
                    ),
                    "new_clients_count": await self._get_clients_count(
                        session=session,
                        user_id=user_id,
                        current_date=current_date,
                        next_date=next_date,
                    ),
                    "avg_order_price": await self._get_avg_order_price(
                        session=session,
                        user_id=user_id,
                        current_date=current_date,
                        next_date=next_date,
                    ),
                    "avg_order_time": await self._get_avg_order_time(
                        session=session,
                        user_id=user_id,
                        current_date=current_date,
                        next_date=next_date,
                    ),
                }
            )

            current_date = next_date

        return statistics
