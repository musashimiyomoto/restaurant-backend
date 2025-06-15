import uuid

import pytest

from settings import auth_settings
from tests.factories import ClientFactory
from tests.test_api.base import BaseTestCase
from utils.crypto import pwd_context


class TestClientAuthRegister(BaseTestCase):
    url = "/auth/register"

    def _client_data(self, user_id: int) -> dict:
        return {
            "user_id": user_id,
            "email": f"client-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
            "first_name": "John",
            "last_name": "Doe",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, _ = await self.create_user_and_get_token()
        client_data = self._client_data(user_id=user["id"])

        response = await self.client.post(url=self.url, json=client_data)

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["user_id"] == client_data["user_id"]
        assert data["email"] == client_data["email"]
        assert data["first_name"] == client_data["first_name"]
        assert data["last_name"] == client_data["last_name"]
        assert data["is_active"] is True
        assert "created_at" in data
        assert "password" not in data
        assert "hashed_password" not in data


class TestClientAuthToken(BaseTestCase):
    url = "/auth/token"

    def _client_data(self) -> dict:
        return {
            "email": f"client-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, _ = await self.create_user_and_get_token()
        client_data = self._client_data()
        await ClientFactory.create_async(
            session=self.session,
            email=client_data["email"],
            hashed_password=pwd_context.hash(client_data["password"]),
            user_id=user["id"],
        )

        response = await self.client.post(
            url=self.url,
            json={"email": client_data["email"], "password": client_data["password"]},
        )

        data = await self.assert_response_ok(response=response)
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == auth_settings.token_type
