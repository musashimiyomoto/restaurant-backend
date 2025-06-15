from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants.db import TEXT_LENGTH
from db.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Category ID"
    )

    user_id: Mapped[int] = mapped_column(index=True, comment="User ID")
    parent_id: Mapped[int | None] = mapped_column(index=True, comment="Parent ID")

    name: Mapped[str] = mapped_column(
        String(length=TEXT_LENGTH), comment="Category name"
    )
    is_type: Mapped[bool] = mapped_column(default=False, comment="Is type category")
    is_sub_type: Mapped[bool] = mapped_column(default=False, comment="Is sub type")
