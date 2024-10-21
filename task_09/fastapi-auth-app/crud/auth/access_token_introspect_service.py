
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.models import AccessToken, User

from .base_token_validation_service import BaseTokenValidationService


class AccessTokenIntrospectService(BaseTokenValidationService[AccessToken]):

    async def fetch_access_token(self) -> AccessToken | None:
        stmt = (
            select(AccessToken)
            .options(
                joinedload(AccessToken.user)
                # Load only id and username from User
                .load_only(User.id, User.username)
            )
            .where(AccessToken.token == self.token)
        )

        access_token: AccessToken | None = await self.session.scalar(stmt)
        return access_token

    async def act(self) -> AccessToken:
        return await self.get_validated_token()
