import pytest

from tests.factories import DeliveryFactory
from tests.test_api.base import BaseTestCase


class TestClientDeliveryList(BaseTestCase):
    url = "/delivery/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        delivery_length = 2
        client, headers = await self.create_client_and_get_token()
        await DeliveryFactory.create_async(
            session=self.session, user_id=client["user_id"]
        )
        await DeliveryFactory.create_async(
            session=self.session, user_id=client["user_id"]
        )

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == delivery_length
        assert all("id" in item for item in data)
        assert all("radius_from" in item for item in data)
        assert all("radius_to" in item for item in data)
        assert all("delivery_time" in item for item in data)
        assert all("price" in item for item in data)
