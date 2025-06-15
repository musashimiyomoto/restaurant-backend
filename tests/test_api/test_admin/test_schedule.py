import pytest

from enums.date import DayEnum
from tests.factories import ScheduleFactory
from tests.test_api.base import BaseTestCase


class TestAdminScheduleList(BaseTestCase):
    url = "/admin/schedule"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        schedule_length = 2
        user, headers = await self.create_user_and_get_token()
        await ScheduleFactory.create_async(session=self.session, user_id=user["id"])
        await ScheduleFactory.create_async(session=self.session, user_id=user["id"])

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == schedule_length
        assert all("id" in item for item in data)
        assert all("day" in item for item in data)
        assert all("start" in item for item in data)
        assert all("end" in item for item in data)


class TestAdminScheduleCreate(BaseTestCase):
    url = "/admin/schedule/create"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        _, headers = await self.create_user_and_get_token()
        schedule_data = {
            "day": DayEnum.WEDNESDAY.value,
            "start": "09:00:00",
            "end": "18:00:00",
        }

        response = await self.client.post(
            url=self.url, json=schedule_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["day"] == schedule_data["day"]
        assert data["start"] == schedule_data["start"]
        assert data["end"] == schedule_data["end"]


class TestAdminScheduleUpdate(BaseTestCase):
    url = "/admin/schedule/{day}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        day = DayEnum.THURSDAY
        user, headers = await self.create_user_and_get_token()
        schedule = await ScheduleFactory.create_async(
            session=self.session, day=day, user_id=user["id"]
        )
        update_data = {"start": "10:00:00", "end": "20:00:00"}

        response = await self.client.put(
            url=self.url.format(day=day.value), json=update_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == schedule.id
        assert data["start"] == update_data["start"]
        assert data["end"] == update_data["end"]
        assert data["day"] == day.value
