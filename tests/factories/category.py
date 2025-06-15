import factory

from db.models.category import Category

from .base import AsyncSQLAlchemyModelFactory, fake


class CategoryFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Category

    user_id = factory.Sequence(lambda n: n + 1)
    parent_id = None
    name = factory.LazyAttribute(lambda obj: fake.word().capitalize())
    is_type = False
    is_sub_type = False
