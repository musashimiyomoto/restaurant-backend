from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from enums.order import OrderStatusEnum


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Order ID"
    )

    client_id: Mapped[int] = mapped_column(index=True, comment="Client ID")
    user_id: Mapped[int] = mapped_column(index=True, comment="User ID")

    status: Mapped[OrderStatusEnum] = mapped_column(comment="Order status")
    check_photo_url: Mapped[str | None] = mapped_column(comment="Check photo URL")
    price: Mapped[Decimal] = mapped_column(comment="Price in currency")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Created at"
    )
