from typing import Annotated, Generic, TypeVar

from fastapi import Depends, Path
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base, db_helper
from crud.base_service import BaseService

T = TypeVar("T", bound=Base)


class GetObjectDetailsService(
    BaseService[T | None],
    Generic[T],
):
    model: type[T]

    def __init__(
        self,
        object_id: Annotated[
            PositiveInt,
            Path(alias="id"),
        ],
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ) -> None:
        self.object_id = object_id
        self.session = session

    async def act(self) -> T | None:
        return await self.session.get(self.model, self.object_id)
