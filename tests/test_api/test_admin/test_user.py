import uuid

import pytest

from enums.role import UserRoleEnum
from tests.factories import UserFactory
from tests.test_api.base import BaseTestCase


class TestAdminUserMe(BaseTestCase):
    url = "/admin/user/me"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert data["id"] == user["id"]
        assert data["email"] == user["email"]
        assert data["role"] == UserRoleEnum.ADMIN


class TestAdminUserList(BaseTestCase):
    url = "/admin/user/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        users = [
            await UserFactory.create_async(
                session=self.session, parent_id=user["id"], role=role
            )
            for role in UserRoleEnum
        ]

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == len(users)


class TestAdminUserCreate(BaseTestCase):
    url = "/admin/user/create/{role}"

    def _user_data(self) -> dict:
        return {
            "name": "New User",
            "email": f"newuser-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
            "photo_url": "https://example.com/photo.jpg",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        user_data = self._user_data()

        response = await self.client.post(
            url=self.url.format(role=UserRoleEnum.HOSTESS),
            json=user_data,
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["role"] == UserRoleEnum.HOSTESS
        assert data["parent_id"] == user["id"]
