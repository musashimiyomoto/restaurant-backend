from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from constants.db import TEXT_LENGTH
from db.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Client ID"
    )

    user_id: Mapped[int] = mapped_column(index=True, comment="User ID")

    email: Mapped[str | None] = mapped_column(unique=True, comment="Client email")
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger(), unique=True, comment="Client telegram ID"
    )
    telegram_username: Mapped[str | None] = mapped_column(
        unique=True, comment="Client telegram username"
    )
    first_name: Mapped[str | None] = mapped_column(
        String(length=TEXT_LENGTH), comment="Client first name"
    )
    last_name: Mapped[str | None] = mapped_column(
        String(length=TEXT_LENGTH), comment="Client last name"
    )

    hashed_password: Mapped[str | None] = mapped_column(comment="Hashed password")

    is_active: Mapped[bool | None] = mapped_column(default=True, comment="Is active")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Created at"
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), comment="Last login"
    )
