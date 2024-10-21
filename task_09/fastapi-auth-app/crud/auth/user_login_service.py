from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AccessToken, User, db_helper
from core.schemas.user import UserLogin
from crud.base_service import BaseService


class UserLoginService(BaseService[AccessToken | None]):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        user_login: UserLogin,
    ) -> None:
        self.session = session
        self.user_login = user_login

    async def get_validated_user(self) -> User | None:
        stmt = select(User).where(User.username == self.user_login.username)
        user: User | None = await self.session.scalar(stmt)
        if user and user.validate_password(password=self.user_login.password):
            return user
        return None

    async def act(self) -> AccessToken | None:
        user: User | None = await self.get_validated_user()
        if not user:
            return None

        access_token = AccessToken(user_id=user.id)
        self.session.add(access_token)
        await self.session.commit()
        await self.session.refresh(access_token)
        return access_token
