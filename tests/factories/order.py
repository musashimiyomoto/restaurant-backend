from decimal import Decimal

from factory.declarations import LazyAttribute, Sequence

from db.models.order import Order
from enums.order import OrderStatusEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class OrderFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Order

    client_id = Sequence(lambda n: n + 1)
    user_id = Sequence(lambda n: n + 1)
    status = OrderStatusEnum.CLIENT_NEW
    price = LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
