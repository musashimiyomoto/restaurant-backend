from db.models import Delivery
from repositories.base import BaseRepository


class DeliveryRepository(BaseRepository[Delivery]):
    def __init__(self):
        super().__init__(Delivery)
