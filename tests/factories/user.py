import factory

from db.models.user import User
from enums.currency import CurrencyEnum
from enums.role import UserRoleEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    name = factory.LazyAttribute(lambda obj: fake.name())
    email = factory.LazyAttribute(lambda obj: fake.email())
    telegram_id = factory.LazyAttribute(
        lambda obj: fake.random_int(min=1000000000, max=9999999999)
    )
    telegram_username = factory.LazyAttribute(lambda obj: fake.user_name())
    photo_url = factory.LazyAttribute(lambda obj: fake.image_url())
    currency = CurrencyEnum.RUB
    parent_id = None
    hashed_password = factory.LazyAttribute(lambda obj: fake.password())
    role = UserRoleEnum.ADMIN
    is_active = True

    @factory.post_generation
    def set_hashed_password(obj, create, extracted, **kwargs):
        if extracted:
            obj.hashed_password = f"hashed_{extracted}"
