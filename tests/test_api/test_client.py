import pytest

from tests.test_api.base import BaseTestCase


class TestClientMe(BaseTestCase):
    url = "/client/me"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        client, headers = await self.create_client_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert data["id"] == client["id"]
        assert data["user_id"] == client["user_id"]
        assert data["email"] == client["email"]
        assert data["first_name"] == client["first_name"]
        assert data["last_name"] == client["last_name"]
        assert data["is_active"] == client["is_active"]
        assert "created_at" in data
