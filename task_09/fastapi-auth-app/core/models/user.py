from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .access_token import AccessToken


class User(IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)

    access_tokens: Mapped[list["AccessToken"]] = relationship(
        back_populates="user",
    )
