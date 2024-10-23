from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.schemas.token_introspect import TokenIntrospect
from crud.base_service import BaseService
from crud.user_details.get_optional_token_introspect_service import (
    get_optional_token_introspect,
)


class GetOptionalCurrentUserService(BaseService[User | None]):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        token: TokenIntrospect | None = Depends(get_optional_token_introspect),
    ) -> None:
        self.token: TokenIntrospect | None = token
        self.session = session

    async def act(self) -> User | None:
        if not self.token:
            return None
        stmt = select(User).where(User.username == self.token.username)
        user: User | None = await self.session.scalar(stmt)
        return user
