from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from core.schemas.token_introspect import TokenIntrospect
from crud.auth_token.token_introspect_service import (
    InvalidTokenError,
    TokenIntrospectService,
)
from crud.base_service import BaseService


class GetOptionalTokenIntrospectService(BaseService[TokenIntrospect | None]):
    def __init__(
        self,
        token: HTTPAuthorizationCredentials | None = Depends(
            HTTPBearer(auto_error=False)
        ),
    ) -> None:
        self.token: str | None = None
        if token:
            self.token = token.credentials

    async def act(self) -> TokenIntrospect | None:
        if not self.token:
            return None
        introspect = TokenIntrospectService(token=self.token)
        return await introspect()


async def get_optional_token_introspect(
    introspect: Annotated[
        GetOptionalTokenIntrospectService,
        Depends(GetOptionalTokenIntrospectService),
    ],
) -> TokenIntrospect | None:
    try:
        return await introspect()
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        )


async def get_required_token_introspect(
    introspect: Annotated[
        TokenIntrospect | None,
        Depends(get_optional_token_introspect),
    ],
) -> TokenIntrospect:
    if introspect:
        return introspect
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not authorized",
    )
