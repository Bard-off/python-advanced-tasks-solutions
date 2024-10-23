from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from core.models import User, db_helper
from core.schemas.token_introspect import TokenIntrospect
from crud.base_service import BaseService
from crud.user_details.get_optional_token_introspect_service import (
    get_required_token_introspect,
)


class GetUserPrivateDetailsService(BaseService[User | None]):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        token: TokenIntrospect = Depends(get_required_token_introspect),
    ) -> None:
        self.session = session
        self.token = token

    async def act(self) -> User | None:
        # username or email? your choice
        stmt = (
            select(User)
            .options(
                joinedload(User.address),
            )
            .where(
                User.email == self.token.username,
            )
        )
        user: User | None = await self.session.scalar(stmt)
        return user


async def get_current_user_private_details(
    get_user: Annotated[
        GetUserPrivateDetailsService,
        Depends(GetUserPrivateDetailsService),
    ],
) -> User:
    user: User | None = await get_user()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found.",
    )
