from decimal import Decimal

import pytest

from enums.order import OrderStatusEnum
from tests.factories import CategoryFactory, DishFactory, OrderFactory
from tests.test_api.base import BaseTestCase


class TestClientOrderList(BaseTestCase):
    url = "/order/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        order_length = 2
        client, headers = await self.create_client_and_get_token()
        await OrderFactory.create_async(
            session=self.session,
            client_id=client["id"],
            user_id=client["user_id"],
        )
        await OrderFactory.create_async(
            session=self.session,
            client_id=client["id"],
            user_id=client["user_id"],
        )

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == order_length
        assert all("id" in item for item in data)
        assert all("status" in item for item in data)
        assert all("price" in item for item in data)


class TestClientOrderGetById(BaseTestCase):
    url = "/order/{order_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        client, headers = await self.create_client_and_get_token()
        order = await OrderFactory.create_async(
            session=self.session,
            client_id=client["id"],
            user_id=client["user_id"],
        )

        response = await self.client.get(
            url=self.url.format(order_id=order.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == order.id
        assert data["status"] == order.status
        assert Decimal(data["price"]) == Decimal(order.price)


class TestClientOrderCreate(BaseTestCase):
    url = "/order/create"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        client, headers = await self.create_client_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session,
            user_id=client["user_id"],
        )
        dish = await DishFactory.create_async(
            session=self.session,
            category_id=category.id,
            user_id=client["user_id"],
        )
        order_data = {
            "order_dishes": [
                {
                    "dish_id": dish.id,
                    "quantity": 2,
                    "price": str(dish.price),
                }
            ],
            "check_photo_url": "check_photo_url",
            "price": 100,
        }

        response = await self.client.post(
            url=self.url, json=order_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert "status" in data


class TestClientOrderUpdateStatus(BaseTestCase):
    url = "/order/{order_id}/status/{status}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        expected_status = OrderStatusEnum.CLIENT_OPENED
        client, headers = await self.create_client_and_get_token()
        order = await OrderFactory.create_async(
            session=self.session,
            client_id=client["id"],
            user_id=client["user_id"],
            status=OrderStatusEnum.CLIENT_NEW,
        )

        response = await self.client.patch(
            url=self.url.format(order_id=order.id, status=expected_status.value),
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == order.id
        assert data["status"] == expected_status.value


class TestClientOrderStatusTransitions(BaseTestCase):
    url = "/order/{order_id}/status/transitions"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        client, headers = await self.create_client_and_get_token()
        order = await OrderFactory.create_async(
            session=self.session,
            client_id=client["id"],
            user_id=client["user_id"],
        )

        response = await self.client.get(
            url=self.url.format(order_id=order.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert all("value" in item for item in data)
        assert all("name" in item for item in data)
        assert all("description" in item for item in data)


class TestClientOrderStatusHistory(BaseTestCase):
    url = "/order/{order_id}/status/history"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        client, headers = await self.create_client_and_get_token()
        order = await OrderFactory.create_async(
            session=self.session,
            client_id=client["id"],
            user_id=client["user_id"],
        )

        response = await self.client.get(
            url=self.url.format(order_id=order.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert "order_id" in data
        assert "history" in data
        assert "total_duration_seconds" in data
        assert isinstance(data["history"], list)
