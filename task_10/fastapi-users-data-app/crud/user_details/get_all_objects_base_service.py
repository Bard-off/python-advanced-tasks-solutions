from typing import Annotated, Generic, TypeVar

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models.mixins.int_id_pk import IntIdPkMixin
from crud.base_service import BaseService

T = TypeVar("T", bound=IntIdPkMixin)


class GetAllObjectsBaseService(
    BaseService[list[T]],
    Generic[T],
):
    model: type[T]

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ) -> None:
        self.session = session

    async def act(self) -> list[T]:
        stmt = select(self.model).order_by(self.model.id)
        result = await self.session.scalars(stmt)
        return list(result.all())
