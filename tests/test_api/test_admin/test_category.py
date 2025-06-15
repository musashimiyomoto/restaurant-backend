import pytest

from tests.factories import CategoryFactory
from tests.test_api.base import BaseTestCase


class TestAdminCategoryList(BaseTestCase):
    url = "/admin/category/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        category_length = 2
        user, headers = await self.create_user_and_get_token()
        await CategoryFactory.create_async(session=self.session, user_id=user["id"])
        await CategoryFactory.create_async(session=self.session, user_id=user["id"])

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == category_length
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)


class TestAdminCategoryCreate(BaseTestCase):
    url = "/admin/category/create"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        _, headers = await self.create_user_and_get_token()
        category_data = {
            "name": "New Test Category",
            "is_type": True,
            "is_sub_type": False,
        }

        response = await self.client.post(
            url=self.url, json=category_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["name"] == category_data["name"]
        assert data["is_type"] == category_data["is_type"]
        assert data["is_sub_type"] == category_data["is_sub_type"]


class TestAdminCategoryUpdate(BaseTestCase):
    url = "/admin/category/{category_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session, user_id=user["id"]
        )
        update_data = {"name": "Updated Category", "is_type": True}

        response = await self.client.put(
            url=self.url.format(category_id=category.id),
            json=update_data,
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == category.id
        assert data["name"] == update_data["name"]
        assert data["is_type"] == update_data["is_type"]


class TestAdminCategoryDelete(BaseTestCase):
    url = "/admin/category/{category_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session, user_id=user["id"]
        )

        response = await self.client.delete(
            url=self.url.format(category_id=category.id), headers=headers
        )

        await self.assert_response_no_content(response=response)
