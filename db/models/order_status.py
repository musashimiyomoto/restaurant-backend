from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from enums.order import OrderStatusEnum


class OrderStatus(Base):
    __tablename__ = "order_status"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "status",
            name="uq_order_status_order_id_status",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Order status ID"
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), index=True, comment="Order ID"
    )
    status: Mapped[OrderStatusEnum] = mapped_column(comment="Order status")

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Start date"
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="End date"
    )

    changed_by_user_id: Mapped[int | None] = mapped_column(
        nullable=True, comment="Changed by user ID"
    )
    changed_by_client_id: Mapped[int | None] = mapped_column(
        nullable=True, comment="Changed by client ID"
    )
