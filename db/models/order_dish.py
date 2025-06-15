from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class OrderDish(Base):
    __tablename__ = "order_dishes"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Order dish ID"
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), index=True, comment="Order ID"
    )
    dish_id: Mapped[int] = mapped_column(
        ForeignKey("dishes.id"), index=True, comment="Dish ID"
    )

    quantity: Mapped[int] = mapped_column(comment="Quantity")
    price: Mapped[Decimal] = mapped_column(comment="Price in currency")
