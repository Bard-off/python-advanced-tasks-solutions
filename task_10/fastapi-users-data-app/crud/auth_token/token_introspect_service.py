from aiohttp import ClientSession

from core.config import settings
from core.schemas.token_introspect import TokenIntrospect
from crud.base_service import BaseService


class InvalidTokenError(Exception):
    pass


class TokenIntrospectService(BaseService[TokenIntrospect]):
    def __init__(
        self,
        token: str,
    ) -> None:
        self.token: str = token

    async def act(self) -> TokenIntrospect:
        headers = {"Authorization": f"Bearer {self.token}"}
        async with ClientSession(raise_for_status=False) as session:
            async with session.get(
                url=settings.auth_api.introspect_url,
                headers=headers,
            ) as response:
                if not response.ok:
                    raise InvalidTokenError
                return TokenIntrospect(**await response.json())
