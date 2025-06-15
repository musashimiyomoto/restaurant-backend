from decimal import Decimal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants.db import TEXT_LENGTH
from db.models.base import Base


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Dish ID"
    )

    user_id: Mapped[int] = mapped_column(index=True, comment="User ID")
    category_id: Mapped[int] = mapped_column(index=True, comment="Category ID")

    price: Mapped[Decimal] = mapped_column(comment="Price in currency")
    weight: Mapped[Decimal] = mapped_column(comment="Weight in grams")
    photo_url: Mapped[str | None] = mapped_column(comment="Photo URL")
    name: Mapped[str] = mapped_column(String(length=TEXT_LENGTH), comment="Dish name")
    description: Mapped[str | None] = mapped_column(comment="Dish description")
