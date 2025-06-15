from enum import IntEnum


class OrderStatusEnum(IntEnum):
    description: str

    def __new__(cls, value: int, description: str) -> "OrderStatusEnum":
        obj = int.__new__(cls, value)

        obj._value_ = value
        obj.description = description

        return obj

    # Client-side initial states
    CLIENT_NEW = 0, "На стороне клиента: новый, не открыт"
    CLIENT_OPENED = 1, "На стороне клиента: создан"
    CLIENT_CANCELLED = 2, "На стороне клиента: отменен"

    # Order processing flow
    PENDING_CONFIRMATION = 10, "На стороне ресторана: ожидает подтверждения"
    CONFIRMED = 11, "На стороне ресторана: подтвержден"
    CANCELLED = 12, "На стороне ресторана: отменен"
    COOKING = 20, "На стороне ресторана: готовится"

    # Delivery flow
    WAITING_COURIER = 30, "Ожидает курьера"
    WAITING_SERVER = 31, "Ожидает официанта"
    WAITING_PICKUP = 32, "Ожидает вас"
    DELIVERY_IN_PROGRESS = 40, "В пути к вам"
    ON_TABLE = 41, "Летит к вам на стол"

    # Final states
    DELIVERED = 50, "Выдан"
    RECEIVED = 60, "Получен"
    CONSUMED = 70, "Скушан"
    RATED = 80, "Оценен"
