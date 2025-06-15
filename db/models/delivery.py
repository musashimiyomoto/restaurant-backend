from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Delivery ID"
    )

    user_id: Mapped[int] = mapped_column(index=True, comment="User ID")

    radius_from: Mapped[float] = mapped_column(comment="Radius from in kilometers")
    radius_to: Mapped[float] = mapped_column(comment="Radius to in kilometers")

    delivery_time: Mapped[int] = mapped_column(comment="Delivery time in minutes")

    price: Mapped[Decimal] = mapped_column(comment="Price in currency")
