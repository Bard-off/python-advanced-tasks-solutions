from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user import User


class UserAddress(IntIdPkMixin, Base):
    __table_name_plural_suffix__ = "es"

    street: Mapped[str]
    suite: Mapped[str]
    city: Mapped[str]
    zipcode: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="address",
    )
