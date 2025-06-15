import pytest

from enums.statistics import StatisticsIntervalEnum
from tests.test_api.base import BaseTestCase


class TestAdminStatistics(BaseTestCase):
    url = "/admin/statistics"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        _, headers = await self.create_user_and_get_token()
        params = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "interval": StatisticsIntervalEnum.DAILY.value,
        }

        response = await self.client.get(url=self.url, params=params, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert "date_min" in data
        assert "date_max" in data
        assert "totals" in data
        assert "periods" in data
        assert "interval" in data
        assert isinstance(data["periods"], list)
        assert isinstance(data["totals"], dict)
