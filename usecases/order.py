from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from constants.order import (
    CLIENT_ONLY_STATUSES,
    ROLE_STATUS_PERMISSIONS,
    STATUS_CHECK_ADMIN_ROLES,
)
from db.models import Order
from enums.order import OrderStatusEnum
from enums.redis import RedisChannelEnum
from enums.role import UserRoleEnum
from repositories import (
    OrderDishRepository,
    OrderRepository,
    OrderStatusRepository,
    UserRepository,
)
from schemas import (
    ClientResponseSchema,
    OrderCreateSchema,
    OrderDishResponseSchema,
    OrderFilterSchema,
    OrderResponseSchema,
    OrderStatusHistoryResponseSchema,
    OrderStatusResponseSchema,
    admin,
)
from utils.redis import publish_to_channel


class OrderUsecase:
    def __init__(self):
        self._order_repository = OrderRepository()
        self._order_dish_repository = OrderDishRepository()
        self._order_status_repository = OrderStatusRepository()
        self._user_repository = UserRepository()

    async def _get_order(
        self, session: AsyncSession, order_id: int, **filters
    ) -> Order:
        """Get an order by id.

        Args:
            session: The session.
            order_id: The order ID.
            filters: The filters.

        Returns:
            The order.

        Raises:
            ValueError: If the order is not found.

        """
        order = await self._order_repository.get_by(
            session=session, id=order_id, **filters
        )
        if not order:
            msg = f"Order with id {order_id} not found"
            raise ValueError(msg)
        return order

    @staticmethod
    def _check_permissions(
        order: Order,
        current_user: admin.UserResponseSchema | None = None,
        current_client: ClientResponseSchema | None = None,
    ) -> None:
        """Check if the user has permissions to update the order.

        Args:
            order: The order.
            current_user: The current user if it's admin.
            current_client: The current client if it's client.

        Raises:
            ValueError: If the user is not allowed to access the order.

        """
        if current_user and order.user_id not in [
            current_user.id,
            current_user.parent_id,
        ]:
            msg = (
                f"User with id {current_user.id} is not allowed"
                f" to access order with id {order.id}"
            )
            raise ValueError(msg)
        if current_client and order.client_id != current_client.id:
            msg = (
                f"Client with id {current_client.id} is not allowed"
                f" to access order with id {order.id}"
            )
            raise ValueError(msg)

    @staticmethod
    def _get_available_status_transitions(
        order: Order, user_role: UserRoleEnum | None = None
    ) -> list[OrderStatusEnum]:
        """Get available status transitions for an order based on user role.

        Args:
            order: The order.
            user_role: The user role.

        Returns:
            The available status transitions.

        """
        status_permissions = (
            ROLE_STATUS_PERMISSIONS.get(user_role, {})
            if user_role
            else CLIENT_ONLY_STATUSES
        )
        return status_permissions.get(order.status, [])

    @staticmethod
    async def _publish_update_order_status(
        order_status: OrderStatusEnum, order_id: int, user_id: int
    ) -> None:
        """Publish an update order status event.

        Args:
            order_status: The order status.
            order_id: The order ID.

        """
        for role in STATUS_CHECK_ADMIN_ROLES.get(order_status, []):
            await publish_to_channel(
                channel=RedisChannelEnum.ORDER_STATUS_UPDATED.value.format(
                    user_id=user_id, role=role.value
                ),
                message=str(order_id),
            )

    @staticmethod
    def _generate_filters(
        base_filters: dict[str, Any],
        user_id: int | None,
        client_id: int | None,
        is_admin: bool,
    ) -> dict:
        """Get the filter data.

        Args:
            base_filters: The base filters.
            user_id: The user ID.
            client_id: The client ID.
            is_admin: Whether the user is admin.

        Returns:
            The filter data.

        """
        filters = {**base_filters}
        if client_id:
            filters["client_id"] = client_id
        if is_admin:
            if user_id:
                filters["user_id"] = user_id
            else:
                filters["parent_id"] = user_id
        return filters

    async def get_orders(
        self,
        session: AsyncSession,
        filters: OrderFilterSchema | admin.OrderFilterSchema,
        client_id: int | None = None,
        user_id: int | None = None,
        is_admin: bool = False,
    ) -> list[OrderResponseSchema]:
        """Get the orders.

        Args:
            session: The session.
            filters: The filters.
            client_id: The client ID.
            user_id: The user ID.
            is_admin: Whether the user is admin.

        Returns:
            The orders.

        """
        return [
            OrderResponseSchema(
                id=order.id,
                client_id=order.client_id,
                status=order.status,
                check_photo_url=order.check_photo_url,
                price=order.price,
                order_dishes=list(
                    map(
                        OrderDishResponseSchema.model_validate,
                        await self._order_dish_repository.get_all(
                            session=session, order_id=order.id
                        ),
                    )
                ),
                created_at=order.created_at,
            )
            for order in await self._order_repository.get_all(
                session=session,
                **self._generate_filters(
                    base_filters=filters.model_dump(exclude_none=True),
                    client_id=client_id,
                    user_id=user_id,
                    is_admin=is_admin,
                ),
            )
        ]

    async def get_order_by_id(
        self,
        session: AsyncSession,
        order_id: int,
        user_id: int | None = None,
        client_id: int | None = None,
        is_admin: bool = False,
    ) -> OrderResponseSchema:
        """Get an order.

        Args:
            session: The session.
            order_id: The order ID.
            user_id: The user ID.
            client_id: The client ID.
            is_admin: Whether the user is admin.

        Returns:
            The order.

        """
        order = await self._get_order(
            session=session,
            order_id=order_id,
            **self._generate_filters(
                base_filters={},
                client_id=client_id,
                user_id=user_id,
                is_admin=is_admin,
            ),
        )

        return OrderResponseSchema(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            check_photo_url=order.check_photo_url,
            price=order.price,
            order_dishes=list(
                map(
                    OrderDishResponseSchema.model_validate,
                    await self._order_dish_repository.get_all(
                        session=session, order_id=order.id
                    ),
                )
            ),
            created_at=order.created_at,
        )

    async def create_order(
        self,
        session: AsyncSession,
        data: OrderCreateSchema,
        client_id: int,
        user_id: int,
    ) -> OrderResponseSchema:
        """Create an order.

        Args:
            session: The session.
            data: The data.
            client_id: The client ID.
            user_id: The user ID.

        """
        order = await self._order_repository.create(
            session=session,
            data={
                **data.model_dump(exclude_none=True, exclude={"order_dishes"}),
                "client_id": client_id,
                "user_id": user_id,
                "status": OrderStatusEnum.CLIENT_NEW,
            },
        )

        await self._order_status_repository.create(
            session=session,
            data={
                "order_id": order.id,
                "status": OrderStatusEnum.CLIENT_NEW,
                "changed_by_client_id": client_id,
            },
        )

        await self._order_dish_repository.create_with_dishes(
            session=session,
            order_id=order.id,
            data=[
                order_dish.model_dump(exclude_none=True)
                for order_dish in data.order_dishes
            ],
        )

        return OrderResponseSchema.model_validate(order)

    async def update_order_status(
        self,
        session: AsyncSession,
        order_id: int,
        new_status: OrderStatusEnum,
        current_user: admin.UserResponseSchema | None = None,
        current_client: ClientResponseSchema | None = None,
    ) -> OrderResponseSchema:
        """Update the order status according to the status flow and user role
        permissions.

        Args:
            session: The session.
            order_id: The order ID.
            new_status: The new status to set.
            current_user: The current user if it's admin.
            current_client: The current client if it's client.

        Returns:
            The updated order.

        Raises:
            ValueError: If the status transition is not allowed.
            ValueError: If the user role doesn't have permission to make this change.

        """
        if new_status not in await self.get_available_status_transitions(
            session=session,
            order_id=order_id,
            current_user=current_user,
            current_client=current_client,
        ):
            msg = "Invalid status transition"
            raise ValueError(msg)

        await self._order_status_repository.close_previous_status(
            session=session, order_id=order_id, end_date=datetime.now(tz=UTC)
        )

        await self._order_status_repository.create(
            session=session,
            data={
                "order_id": order_id,
                "status": new_status,
                "changed_by_user_id": current_user.id if current_user else None,
                "changed_by_client_id": current_client.id if current_client else None,
            },
        )

        order = await self._order_repository.update_by(
            session=session,
            data={"status": new_status},
            id=order_id,
        )

        if order is None:
            msg = "Order not found"
            raise ValueError(msg)

        user_id = (
            current_user.id
            if current_user
            else (current_client.user_id if current_client else None)
        )
        if user_id is None:
            msg = "No valid user or client found"
            raise ValueError(msg)

        await self._publish_update_order_status(
            order_status=new_status,
            order_id=order_id,
            user_id=user_id,
        )

        return OrderResponseSchema(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            check_photo_url=order.check_photo_url,
            price=order.price,
            order_dishes=list(
                map(
                    OrderDishResponseSchema.model_validate,
                    await self._order_dish_repository.get_all(
                        session=session, order_id=order.id
                    ),
                )
            ),
            created_at=order.created_at,
        )

    async def get_available_status_transitions(
        self,
        session: AsyncSession,
        order_id: int,
        current_user: admin.UserResponseSchema | None = None,
        current_client: ClientResponseSchema | None = None,
    ) -> list[OrderStatusEnum]:
        """Get available status transitions for an order based on user role.

        Args:
            session: The session.
            order_id: The order ID.
            current_user: The current user if it's admin.
            current_client: The current client if it's client.

        Returns:
            List of available status transitions for the user's role.

        Raises:
            ValueError: If the order is not found.

        """
        order = await self._get_order(session=session, order_id=order_id)

        self._check_permissions(
            order=order, current_user=current_user, current_client=current_client
        )

        return self._get_available_status_transitions(
            order=order, user_role=current_user.role if current_user else None
        )

    async def get_order_status_history(
        self,
        session: AsyncSession,
        order_id: int,
        current_user: admin.UserResponseSchema | None = None,
        current_client: ClientResponseSchema | None = None,
    ) -> OrderStatusHistoryResponseSchema:
        """Get the order status history.

        Args:
            session: The database session.
            order_id: The order ID.
            current_user: The current user if it's admin.
            current_client: The current client if it's client.

        Returns:
            The order with the full status history.

        Raises:
            ValueError: If the order is not found or the user doesn't have access.

        """
        order = await self._get_order(session=session, order_id=order_id)

        self._check_permissions(
            order=order, current_user=current_user, current_client=current_client
        )

        history = [
            OrderStatusResponseSchema(
                status=entry.status,
                start_date=entry.start_date,
                end_date=entry.end_date,
                changed_by_user_id=entry.changed_by_user_id,
                changed_by_client_id=entry.changed_by_client_id,
                duration_seconds=(
                    int((entry.end_date - entry.start_date).total_seconds())
                    if entry.end_date
                    else None
                ),
            )
            for entry in await self._order_status_repository.get_all(
                session=session, order_id=order_id
            )
        ]

        return OrderStatusHistoryResponseSchema(
            order_id=order.id,
            history=history,
            total_duration_seconds=sum(item.duration_seconds or 0 for item in history),
        )
