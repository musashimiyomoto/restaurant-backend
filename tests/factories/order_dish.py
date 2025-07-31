from decimal import Decimal

from factory.declarations import LazyAttribute, Sequence

from db.models.order_dish import OrderDish

from .base import AsyncSQLAlchemyModelFactory, fake


class OrderDishFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = OrderDish

    order_id = Sequence(lambda n: n + 1)
    dish_id = Sequence(lambda n: n + 1)
    quantity = LazyAttribute(lambda obj: fake.random_int(min=1, max=5))
    price = LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
