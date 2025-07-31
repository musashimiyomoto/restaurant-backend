from factory.declarations import Sequence

from db.models.order_status import OrderStatus
from enums.order import OrderStatusEnum

from .base import AsyncSQLAlchemyModelFactory


class OrderStatusFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = OrderStatus

    order_id = Sequence(lambda n: n + 1)
    status = OrderStatusEnum.CLIENT_NEW
    changed_by_user_id = None
    changed_by_client_id = None
