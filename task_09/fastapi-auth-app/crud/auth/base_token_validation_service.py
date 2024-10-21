from abc import ABCMeta
from typing import Annotated, Generic

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AccessToken, db_helper
from crud.auth.access_token_header import http_bearer
from crud.base_service import BaseService, ReturnType


class TokenInvalidError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class BaseTokenValidationService(
    BaseService[ReturnType],
    Generic[ReturnType],
    metaclass=ABCMeta,
):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        access_token: Annotated[
            HTTPAuthorizationCredentials,
            Depends(http_bearer),
        ],
    ) -> None:
        self.session = session
        self.token = access_token.credentials

    async def fetch_access_token(self) -> AccessToken | None:
        stmt = select(AccessToken).where(AccessToken.token == self.token)
        access_token: AccessToken | None = await self.session.scalar(stmt)
        return access_token

    async def get_validated_token(self) -> AccessToken:
        access_token = await self.fetch_access_token()
        if not access_token:
            raise TokenInvalidError
        if not access_token.is_valid:
            raise TokenExpiredError
        return access_token
