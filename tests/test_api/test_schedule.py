import pytest

from tests.factories import ScheduleFactory
from tests.test_api.base import BaseTestCase


class TestClientScheduleList(BaseTestCase):
    url = "/schedule"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        schedule_length = 2
        client, headers = await self.create_client_and_get_token()
        await ScheduleFactory.create_async(
            session=self.session,
            user_id=client["user_id"],
        )
        await ScheduleFactory.create_async(
            session=self.session,
            user_id=client["user_id"],
        )

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == schedule_length
        assert all("id" in item for item in data)
        assert all("day" in item for item in data)
        assert all("start" in item for item in data)
        assert all("end" in item for item in data)
