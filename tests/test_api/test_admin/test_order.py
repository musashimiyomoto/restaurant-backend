from decimal import Decimal

import pytest

from enums.order import OrderStatusEnum
from tests.factories import (
    CategoryFactory,
    ClientFactory,
    DishFactory,
    OrderDishFactory,
    OrderFactory,
    OrderStatusFactory,
)
from tests.test_api.base import BaseTestCase


class BaseOrderTestCase(BaseTestCase):
    async def create_test_order_setup(
        self,
        client_email: str = "test@example.com",
        client_first_name: str = "Test",
        client_last_name: str = "Client",
        category_name: str = "Test Category",
        dish_name: str = "Test Dish",
        dish_price: Decimal = Decimal("15.99"),
        dish_weight: Decimal = Decimal(250),
        order_status: OrderStatusEnum = OrderStatusEnum.CLIENT_NEW,
        order_price: Decimal = Decimal("31.98"),
        dish_quantity: int = 2,
        order_length: int = 1,
    ) -> tuple[dict, dict]:
        user, headers = await self.create_user_and_get_token()
        client = await ClientFactory.create_async(
            session=self.session,
            user_id=user["id"],
            email=client_email,
            first_name=client_first_name,
            last_name=client_last_name,
        )
        category = await CategoryFactory.create_async(
            session=self.session,
            user_id=user["id"],
            name=category_name,
        )
        dish = await DishFactory.create_async(
            session=self.session,
            user_id=user["id"],
            category_id=category.id,
            name=dish_name,
            price=dish_price,
            weight=dish_weight,
        )
        orders = []
        for _ in range(order_length):
            order = await OrderFactory.create_async(
                session=self.session,
                client_id=client.id,
                user_id=user["id"],
                status=order_status,
                price=order_price,
            )
            await OrderStatusFactory.create_async(
                session=self.session,
                order_id=order.id,
                status=order_status,
                changed_by_client_id=client.id,
            )
            await OrderDishFactory.create_async(
                session=self.session,
                order_id=order.id,
                dish_id=dish.id,
                price=dish.price,
                quantity=dish_quantity,
            )
            orders.append(order)

        return {
            "user": user,
            "client": client,
            "category": category,
            "dish": dish,
            "orders": orders,
        }, headers


class TestAdminOrderList(BaseOrderTestCase):
    url = "/admin/order/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        order_length = 2
        _, headers = await self.create_test_order_setup(order_length=order_length)

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == order_length
        assert all("id" in item for item in data)
        assert all("status" in item for item in data)
        assert all("price" in item for item in data)


class TestAdminOrderGetById(BaseOrderTestCase):
    url = "/admin/order/{order_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        models, headers = await self.create_test_order_setup(
            client_email="test2@example.com", client_last_name="Client2"
        )
        order = models["orders"][0]

        response = await self.client.get(
            url=self.url.format(order_id=order.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == order.id
        assert data["status"] == order.status
        assert Decimal(data["price"]) == Decimal(order.price)


class TestAdminOrderUpdateStatus(BaseOrderTestCase):
    url = "/admin/order/{order_id}/status/{status}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        new_status = OrderStatusEnum.CLIENT_CANCELLED
        models, headers = await self.create_test_order_setup()
        order = models["orders"][0]

        response = await self.client.patch(
            url=self.url.format(order_id=order.id, status=new_status.value),
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == order.id
        assert data["status"] == new_status.value


class TestAdminOrderStatusTransitions(BaseOrderTestCase):
    url = "/admin/order/{order_id}/status/transitions"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        models, headers = await self.create_test_order_setup(
            client_email="test2@example.com", client_last_name="Client2"
        )
        order = models["orders"][0]

        response = await self.client.get(
            url=self.url.format(order_id=order.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert all("value" in item for item in data)
        assert all("name" in item for item in data)
        assert all("description" in item for item in data)


class TestAdminOrderStatusHistory(BaseOrderTestCase):
    url = "/admin/order/{order_id}/status/history"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        models, headers = await self.create_test_order_setup(
            client_email="test3@example.com", client_last_name="Client3"
        )
        order = models["orders"][0]

        response = await self.client.get(
            url=self.url.format(order_id=order.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert "order_id" in data
        assert "history" in data
        assert "total_duration_seconds" in data
        assert isinstance(data["history"], list)
