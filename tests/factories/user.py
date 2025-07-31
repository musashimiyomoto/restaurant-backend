from factory.declarations import LazyAttribute
from factory.helpers import post_generation

from db.models.user import User
from enums.currency import CurrencyEnum
from enums.role import UserRoleEnum

from .base import AsyncSQLAlchemyModelFactory, fake


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = User

    name = LazyAttribute(lambda obj: fake.name())
    email = LazyAttribute(lambda obj: fake.email())
    telegram_id = LazyAttribute(
        lambda obj: fake.random_int(min=1000000000, max=9999999999)
    )
    telegram_username = LazyAttribute(lambda obj: fake.user_name())
    photo_url = LazyAttribute(lambda obj: fake.image_url())
    currency = CurrencyEnum.RUB
    parent_id = None
    hashed_password = LazyAttribute(lambda obj: fake.password())
    role = UserRoleEnum.ADMIN
    is_active = True

    @post_generation
    def set_hashed_password(self, create, extracted, **kwargs):
        if extracted:
            self.hashed_password = f"hashed_{extracted}"
