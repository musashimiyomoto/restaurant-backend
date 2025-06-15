import pytest

from tests.test_api.base import BaseTestCase


class TestClientUser(BaseTestCase):
    url = "/user"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        client, headers = await self.create_client_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert data["id"] == client["user_id"]
