from typing import Annotated

from fastapi import Depends, Path
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post, db_helper
from crud.base_service import BaseService


class GetUsersPostsService(BaseService[list[Post]]):
    def __init__(
        self,
        user_id: Annotated[
            PositiveInt,
            Path,
        ],
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ) -> None:
        self.user_id = user_id
        self.session = session

    async def act(self) -> list[Post]:
        # validate if user exists?
        stmt = (
            select(Post)
            .where(
                Post.user_id == self.user_id,
            )
            .order_by(Post.id)
        )
        result = await self.session.scalars(stmt)
        return list(result.all())
