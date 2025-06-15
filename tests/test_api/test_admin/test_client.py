import pytest

from tests.test_api.base import BaseTestCase


class TestAdminClientList(BaseTestCase):
    url = "/admin/client/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        _, headers = await self.create_user_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
