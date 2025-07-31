from factory.declarations import LazyAttribute, Sequence

from db.models.category import Category

from .base import AsyncSQLAlchemyModelFactory, fake


class CategoryFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Category

    user_id = Sequence(lambda n: n + 1)
    parent_id = None
    name = LazyAttribute(lambda obj: fake.word().capitalize())
    is_type = False
    is_sub_type = False
