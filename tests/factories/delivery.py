from decimal import Decimal

from factory.declarations import LazyAttribute, Sequence

from db.models.delivery import Delivery

from .base import AsyncSQLAlchemyModelFactory, fake


class DeliveryFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Delivery

    user_id = Sequence(lambda n: n + 1)
    radius_from = LazyAttribute(
        lambda obj: fake.pyfloat(
            left_digits=2, right_digits=2, positive=True, min_value=0.1, max_value=5.0
        )
    )
    radius_to = LazyAttribute(
        lambda obj: fake.pyfloat(
            left_digits=2, right_digits=2, positive=True, min_value=5.1, max_value=20.0
        )
    )
    delivery_time = LazyAttribute(lambda obj: fake.random_int(min=15, max=120))
    price = LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
