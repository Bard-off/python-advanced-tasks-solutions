from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .post import Post
    from .user_address import UserAddress


class User(IntIdPkMixin, Base):
    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)

    address: Mapped["UserAddress"] = relationship(
        back_populates="user",
    )
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )
