from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import LargeBinary
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
    _password: Mapped[bytes] = mapped_column(
        LargeBinary,
        name="password",
    )

    access_tokens: Mapped[list["AccessToken"]] = relationship(
        back_populates="user",
    )

    @classmethod
    def ensure_bytes(cls, value: str | bytes) -> bytes:
        return value if isinstance(value, bytes) else value.encode("utf-8")

    @property
    def password(self) -> bytes:
        return self._password

    @password.setter
    def password(self, value: bytes | str) -> None:
        salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(self.ensure_bytes(value), salt)

    def validate_password(self, password: str | bytes) -> bool:
        return bcrypt.checkpw(
            # password bytes
            self.ensure_bytes(password),
            # hashed value
            self._password,
        )
