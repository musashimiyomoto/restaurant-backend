import uuid
from unittest import mock

import pytest

from enums.role import UserRoleEnum
from settings import auth_settings
from tests.factories import UserFactory
from tests.test_api.base import BaseTestCase
from utils.crypto import pwd_context


class TestAdminAuthRegister(BaseTestCase):
    url = "/admin/auth/register"

    def _user_data(self) -> dict:
        return {
            "name": "John Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
            "photo_url": "https://example.com/photo.jpg",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()

        response = await self.client.post(url=self.url, json=user_data)

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["photo_url"] == user_data["photo_url"]
        assert data["role"] == UserRoleEnum.ADMIN
        assert data["is_active"] is False
        assert data["parent_id"] is None
        assert "created_at" in data
        assert "password" not in data
        assert "hashed_password" not in data


class TestAdminAuthToken(BaseTestCase):
    url = "/admin/auth/token"

    def _user_data(self) -> dict:
        return {
            "name": "John Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
            "photo_url": "https://example.com/photo.jpg",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()
        await UserFactory.create_async(
            session=self.session,
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
            role=UserRoleEnum.ADMIN,
        )

        response = await self.client.post(
            url=self.url,
            json={"email": user_data["email"], "password": user_data["password"]},
        )

        data = await self.assert_response_ok(response=response)
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == auth_settings.token_type


class TestAdminAuthSendEmailCode(BaseTestCase):
    url = "/admin/auth/send/{email}/code"

    def _user_data(self) -> dict:
        return {
            "name": "John Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()
        await UserFactory.create_async(
            session=self.session,
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
            role=UserRoleEnum.ADMIN,
            is_active=False,
        )

        response = await self.client.post(
            url=self.url.format(email=user_data["email"]),
        )

        await self.assert_response_no_content(response=response)


class TestAdminAuthVerifyEmail(BaseTestCase):
    url = "/admin/auth/verify/{email}/{code}"
    code = "123456"

    def _user_data(self) -> dict:
        return {
            "name": "John Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()
        await UserFactory.create_async(
            session=self.session,
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
            role=UserRoleEnum.ADMIN,
            is_active=False,
        )

        with mock.patch(
            "usecases.auth.UserAuthUsecase._generate_code", return_value=self.code
        ):
            await self.client.post(url=f"/admin/auth/send/{user_data['email']}/code")
            response = await self.client.post(
                url=self.url.format(email=user_data["email"], code=self.code)
            )

        await self.assert_response_no_content(response=response)
