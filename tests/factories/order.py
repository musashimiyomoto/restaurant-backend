from decimal import Decimal

import factory

from db.models.order import Order
from enums.order import OrderStatusEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class OrderFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Order

    client_id = factory.Sequence(lambda n: n + 1)
    user_id = factory.Sequence(lambda n: n + 1)
    status = OrderStatusEnum.CLIENT_NEW
    price = factory.LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
