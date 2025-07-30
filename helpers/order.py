import asyncio
import random
from decimal import Decimal
from http import HTTPStatus

import httpx
from faker import Faker

API_BASE_URL = "http://localhost:5000"
NUM_CLIENTS = 5
ORDERS_PER_CLIENT = 3
USER_ID = 1
USER_EMAIL = "iosif.krokai@gmail.com"
USER_PASSWORD = "Krokai123"

fake = Faker(["ru_RU", "en_US"])


class OrderHelper:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.clients = []
        self.sample_dishes = []

    async def create_dishes(self, dishes_count: int = 10) -> list[dict]:
        dishes = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/admin/auth/token",
                json={
                    "email": USER_EMAIL,
                    "password": USER_PASSWORD,
                },
            )
            if response.status_code == HTTPStatus.OK:
                token = response.json()["access_token"]
            else:
                return dishes

            category_ids = []
            response = await client.get(
                f"{self.base_url}/admin/category/list",
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code == HTTPStatus.OK:
                category_ids = [category["id"] for category in response.json()]
            else:
                return dishes

            for _ in range(dishes_count):
                response = await client.post(
                    f"{self.base_url}/admin/image/upload",
                    headers={
                        "Authorization": f"Bearer {token}",
                    },
                    files={
                        "file": open(
                            f"helpers/images/dish_{random.randint(1, 5)}.jpg", "rb"
                        )
                    },
                )
                if response.status_code == HTTPStatus.OK:
                    photo_url = response.json()["url"]
                else:
                    return dishes

                response = await client.post(
                    f"{self.base_url}/admin/dish/create",
                    headers={"Authorization": f"Bearer {token}"},
                    json={
                        "category_id": random.choice(category_ids),
                        "price": random.randint(100, 1000),
                        "weight": random.randint(100, 1000),
                        "photo_url": photo_url,
                        "name": fake.name(),
                        "description": fake.text(),
                    },
                )

                if response.status_code == HTTPStatus.OK:
                    dishes.append(
                        {"id": response.json()["id"], "price": response.json()["price"]}
                    )
                else:
                    pass

        return dishes

    async def create_clients(self, num_clients: int = NUM_CLIENTS):

        async with httpx.AsyncClient(timeout=30.0) as client:
            for _i in range(num_clients):
                client_data = {
                    "user_id": USER_ID,
                    "email": fake.email(),
                    "password": "password123",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                }

                if random.choice([True, False]):
                    client_data.update(
                        {
                            "telegram_id": fake.random_int(
                                min=100000000, max=999999999
                            ),
                            "telegram_username": fake.user_name(),
                        }
                    )

                try:
                    response = await client.post(
                        f"{self.base_url}/auth/register", json=client_data
                    )

                    if response.status_code == HTTPStatus.OK:
                        client_info = response.json()
                        client_data["id"] = client_info["id"]
                        self.clients.append(client_data)
                    else:
                        pass
                except Exception:
                    pass

    async def get_auth_token(self, client_data: dict) -> str | None:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/token",
                    json={
                        "email": client_data["email"],
                        "password": client_data["password"],
                    },
                )

                if response.status_code == HTTPStatus.OK:
                    return response.json()["access_token"]
                return None
            except Exception:
                return None

    async def create_orders_for_client(
        self, client_data: dict, num_orders: int = ORDERS_PER_CLIENT
    ):
        token = await self.get_auth_token(client_data)
        if not token:
            return

        headers = {"Authorization": f"Bearer {token}"}

        for _i in range(num_orders):
            try:
                num_dishes = random.randint(1, 4)
                selected_dishes = random.sample(self.sample_dishes, num_dishes)

                order_dishes = []
                total_price = Decimal(0)

                for dish in selected_dishes:
                    quantity = random.randint(1, 2)
                    dish_price = Decimal(dish["price"])

                    order_dishes.append(
                        {
                            "dish_id": dish["id"],
                            "price": float(dish_price),
                            "quantity": quantity,
                        }
                    )

                    total_price += dish_price * quantity

                order_data = {
                    "price": float(total_price),
                    "check_photo_url": None,
                    "order_dishes": order_dishes,
                }

                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.base_url}/order/create",
                        json=order_data,
                        headers=headers,
                    )

                    if response.status_code == HTTPStatus.OK:
                        status = 1
                        order_id = response.json()["id"]
                        res = await client.patch(
                            f"{self.base_url}/order/{order_id}/status/{status}",
                            headers=headers,
                        )
                        if res.status_code == HTTPStatus.OK:
                            pass
                        else:
                            pass

                    else:
                        pass
            except Exception:
                pass

    async def create_all_orders(self):

        self.sample_dishes = await self.create_dishes()

        for client_data in self.clients:
            await self.create_orders_for_client(client_data=client_data)

    async def run(self):

        await self.create_clients()

        if not self.clients:
            return

        await self.create_all_orders()


async def main():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/docs")
            if response.status_code != HTTPStatus.OK:
                return
    except Exception:
        return

    await OrderHelper().run()


if __name__ == "__main__":
    asyncio.run(main())
