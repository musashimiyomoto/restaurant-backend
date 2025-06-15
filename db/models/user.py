from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from constants.db import TEXT_LENGTH
from db.models.base import Base
from enums.currency import CurrencyEnum
from enums.role import UserRoleEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="User ID"
    )

    name: Mapped[str] = mapped_column(String(length=TEXT_LENGTH), comment="User name")
    email: Mapped[str] = mapped_column(comment="User email")
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger(), comment="User telegram ID"
    )
    telegram_username: Mapped[str | None] = mapped_column(
        comment="User telegram username"
    )
    photo_url: Mapped[str | None] = mapped_column(comment="User photo URL")
    currency: Mapped[CurrencyEnum] = mapped_column(default=CurrencyEnum.RUB)

    parent_id: Mapped[int | None] = mapped_column(index=True, comment="Parent ID")

    hashed_password: Mapped[str | None] = mapped_column(comment="Hashed password")

    role: Mapped[UserRoleEnum] = mapped_column(comment="User role")
    is_active: Mapped[bool] = mapped_column(default=True, comment="Is active")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Created at"
    )
