from decimal import Decimal

from factory.declarations import LazyAttribute, Sequence

from db.models.dish import Dish

from .base import AsyncSQLAlchemyModelFactory, fake


class DishFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Dish

    user_id = Sequence(lambda n: n + 1)
    category_id = Sequence(lambda n: n + 1)
    price = LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )
    )
    weight = LazyAttribute(
        lambda obj: Decimal(
            fake.pydecimal(left_digits=3, right_digits=0, positive=True)
        )
    )
    photo_url = LazyAttribute(lambda obj: fake.image_url())
    name = LazyAttribute(lambda obj: fake.word().capitalize())
    description = LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
