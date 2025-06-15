from decimal import Decimal

import pytest

from tests.factories import CategoryFactory, DishFactory
from tests.test_api.base import BaseTestCase


class TestAdminDishList(BaseTestCase):
    url = "/admin/dish/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        dish_length = 2
        user, headers = await self.create_user_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session, user_id=user["id"]
        )
        await DishFactory.create_async(
            session=self.session, user_id=user["id"], category_id=category.id
        )
        await DishFactory.create_async(
            session=self.session, user_id=user["id"], category_id=category.id
        )

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == dish_length
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)
        assert all("price" in item for item in data)


class TestAdminDishCreate(BaseTestCase):
    url = "/admin/dish/create"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session, user_id=user["id"]
        )
        dish_data = {
            "category_id": category.id,
            "name": "New Test Dish",
            "price": "19.99",
            "weight": "400",
            "description": "Delicious test dish",
        }

        response = await self.client.post(url=self.url, json=dish_data, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["name"] == dish_data["name"]
        assert Decimal(data["price"]) == Decimal(dish_data["price"])
        assert Decimal(data["weight"]) == Decimal(dish_data["weight"])
        assert data["description"] == dish_data["description"]
        assert data["category_id"] == category.id


class TestAdminDishUpdate(BaseTestCase):
    url = "/admin/dish/{dish_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session, user_id=user["id"]
        )
        dish = await DishFactory.create_async(
            session=self.session, user_id=user["id"], category_id=category.id
        )
        update_data = {"name": "Updated Dish", "price": "25.99", "weight": "350"}

        response = await self.client.put(
            url=self.url.format(dish_id=dish.id), json=update_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == dish.id
        assert data["name"] == update_data["name"]
        assert Decimal(data["price"]) == Decimal(update_data["price"])
        assert Decimal(data["weight"]) == Decimal(update_data["weight"])


class TestAdminDishDelete(BaseTestCase):
    url = "/admin/dish/{dish_id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()
        category = await CategoryFactory.create_async(
            session=self.session, user_id=user["id"]
        )
        dish = await DishFactory.create_async(
            session=self.session, user_id=user["id"], category_id=category.id
        )

        response = await self.client.delete(
            url=self.url.format(dish_id=dish.id), headers=headers
        )

        await self.assert_response_no_content(response=response)
