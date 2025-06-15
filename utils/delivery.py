from sqlalchemy.ext.asyncio import AsyncSession

from constants.delivery import DEFAULT_DELIVERIES
from repositories import DeliveryRepository


async def generate_deliveries(session: AsyncSession, user_id: int) -> None:
    """Generate the deliveries in the database.

    Args:
        session: The session of the database.
        user_id: The id of the user.

    """
    delivery_repository = DeliveryRepository()

    for delivery in DEFAULT_DELIVERIES:
        await delivery_repository.create(
            session=session, data={**delivery, "user_id": user_id}
        )
