import io
from pathlib import Path

import pytest

from tests.test_api.base import BaseTestCase


class TestAdminImageUpload(BaseTestCase):
    url = "/admin/image/upload"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        image_content = b"fake_image_content"
        files = {"file": ("test_image.jpg", io.BytesIO(image_content), "image/jpeg")}

        response = await self.client.post(url=self.url, files=files)

        data = await self.assert_response_ok(response=response)
        assert "url" in data
        assert data["url"].startswith("/static/images/")
        assert data["url"].endswith(".jpg")

        image_name = data["url"].split("/")[-1]
        Path(f"static/images/{image_name}").unlink()
