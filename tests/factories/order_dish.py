from decimal import Decimal

import factory

from db.models.order_dish import OrderDish

from .base import AsyncSQLAlchemyModelFactory, fake


class OrderDishFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = OrderDish

    order_id = factory.Sequence(lambda n: n + 1)
    dish_id = factory.Sequence(lambda n: n + 1)
    quantity = factory.LazyAttribute(lambda obj: fake.random_int(min=1, max=5))
    price = factory.LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
