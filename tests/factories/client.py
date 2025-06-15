import factory

from db.models.client import Client

from .base import AsyncSQLAlchemyModelFactory, fake


class ClientFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Client

    user_id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyAttribute(lambda obj: fake.email())
    first_name = factory.LazyAttribute(lambda obj: fake.first_name())
    last_name = factory.LazyAttribute(lambda obj: fake.last_name())
    hashed_password = factory.LazyAttribute(lambda obj: fake.password())
    is_active = True
