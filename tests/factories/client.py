from factory.declarations import LazyAttribute, Sequence

from db.models.client import Client

from .base import AsyncSQLAlchemyModelFactory, fake


class ClientFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Client

    user_id = Sequence(lambda n: n + 1)
    email = LazyAttribute(lambda obj: fake.email())
    first_name = LazyAttribute(lambda obj: fake.first_name())
    last_name = LazyAttribute(lambda obj: fake.last_name())
    hashed_password = LazyAttribute(lambda obj: fake.password())
    is_active = True
