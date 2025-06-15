from decimal import Decimal

import factory

from db.models.dish import Dish

from .base import AsyncSQLAlchemyModelFactory, fake


class DishFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Dish

    user_id = factory.Sequence(lambda n: n + 1)
    category_id = factory.Sequence(lambda n: n + 1)
    price = factory.LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
    weight = factory.LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=0, positive=True)
        )
    )
    photo_url = factory.LazyAttribute(lambda obj: fake.image_url())
    name = factory.LazyAttribute(lambda obj: fake.word().capitalize())
    description = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
