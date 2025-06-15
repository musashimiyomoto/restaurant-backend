from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import OrderStatus
from repositories.base import BaseRepository


class OrderStatusRepository(BaseRepository[OrderStatus]):
    def __init__(self):
        super().__init__(OrderStatus)

    async def close_previous_status(
        self, session: AsyncSession, order_id: int, end_date: datetime
    ) -> None:
        """Close the previous status, setting the end_date.

        Args:
            session: The database session.
            order_id: The order ID.
            end_date: The end date of the previous status.

        """
        result = await session.execute(
            select(OrderStatus)
            .filter_by(order_id=order_id, end_date=None)
            .order_by(OrderStatus.start_date.desc())
            .limit(1)
        )

        last_open_status = result.scalar_one_or_none()

        if last_open_status:
            await session.execute(
                update(OrderStatus)
                .where(OrderStatus.id == last_open_status.id)
                .values(end_date=end_date)
            )
