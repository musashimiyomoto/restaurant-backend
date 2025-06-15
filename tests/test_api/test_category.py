import pytest

from tests.factories import CategoryFactory
from tests.test_api.base import BaseTestCase


class TestClientCategoryList(BaseTestCase):
    url = "/category/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        category_length = 2
        client, headers = await self.create_client_and_get_token()
        await CategoryFactory.create_async(
            session=self.session,
            user_id=client["user_id"],
        )
        await CategoryFactory.create_async(
            session=self.session,
            user_id=client["user_id"],
        )

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == category_length
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)
