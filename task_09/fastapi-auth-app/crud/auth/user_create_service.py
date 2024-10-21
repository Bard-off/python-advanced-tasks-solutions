from typing import Annotated, Any, Callable, Sequence

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.schemas.user import UserRegister
from crud.base_service import BaseService


class UserAlreadyExistsException(Exception):
    pass


class UserCreateService(BaseService[User]):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        user_register: UserRegister,
    ) -> None:
        self.session = session
        self.user_register = user_register

    async def validate_username(self) -> None:
        stmt = select(exists().where(User.username == self.user_register.username))
        username_exists = await self.session.scalar(stmt)
        if username_exists:
            raise UserAlreadyExistsException

    def get_validators(self) -> Sequence[Callable[[], Any]]:
        return [
            self.validate_username,
        ]

    async def act(self) -> User:
        user = User(
            **self.user_register.model_dump(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
