from decimal import Decimal
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Order, OrderDish
from repositories.base import BaseRepository


class OrderDishRepository(BaseRepository[OrderDish]):
    def __init__(self):
        super().__init__(OrderDish)

    async def create_with_dishes(
        self, session: AsyncSession, order_id: int, data: list[dict[str, Any]]
    ) -> None:
        """Create a new order dish.

        Args:
            session: The async session.
            order_id: The id of the order.
            data: The data to create the order dish.

        """
        instances = []
        price = Decimal(0.0)

        for element in data:
            order_dish = self.model(**element)
            order_dish.order_id = order_id
            instances.append(order_dish)
            price += order_dish.price

        session.add_all(instances=instances)
        await session.execute(
            statement=update(Order).filter_by(id=order_id).values({"price": price})
        )
        await session.commit()
