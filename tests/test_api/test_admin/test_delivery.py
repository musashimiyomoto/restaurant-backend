from decimal import Decimal

import pytest

from tests.factories import DeliveryFactory
from tests.test_api.base import BaseTestCase


class TestAdminDeliveryList(BaseTestCase):
    url = "/admin/delivery/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        delivery_length = 2
        user, headers = await self.create_user_and_get_token()
        await DeliveryFactory.create_async(session=self.session, user_id=user["id"])
        await DeliveryFactory.create_async(session=self.session, user_id=user["id"])

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == delivery_length
        assert all("id" in item for item in data)
        assert all("radius_from" in item for item in data)
        assert all("radius_to" in item for item in data)
        assert all("delivery_time" in item for item in data)
        assert all("price" in item for item in data)


class TestAdminDeliveryCreate(BaseTestCase):
    url = "/admin/delivery/create"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        _, headers = await self.create_user_and_get_token()
        delivery_data = {
            "radius_from": 1,
            "radius_to": 2,
            "delivery_time": 25,
            "price": "80.00",
        }

        response = await self.client.post(
            url=self.url, json=delivery_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["radius_from"] == delivery_data["radius_from"]
        assert data["radius_to"] == delivery_data["radius_to"]
        assert data["delivery_time"] == delivery_data["delivery_time"]
        assert Decimal(data["price"]) == Decimal(delivery_data["price"])


class TestAdminDeliveryUpdate(BaseTestCase):
    url = "/admin/delivery/{delivery_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        delivery = await DeliveryFactory.create_async(
            session=self.session, user_id=user["id"]
        )
        update_data = {"radius_to": 3, "delivery_time": 40, "price": "120.00"}

        response = await self.client.put(
            url=self.url.format(delivery_id=delivery.id),
            json=update_data,
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == delivery.id
        assert data["radius_to"] == update_data["radius_to"]
        assert data["delivery_time"] == update_data["delivery_time"]
        assert Decimal(data["price"]) == Decimal(update_data["price"])


class TestAdminDeliveryDelete(BaseTestCase):
    url = "/admin/delivery/{delivery_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        delivery = await DeliveryFactory.create_async(
            session=self.session, user_id=user["id"]
        )

        response = await self.client.delete(
            url=self.url.format(delivery_id=delivery.id), headers=headers
        )

        await self.assert_response_no_content(response=response)
