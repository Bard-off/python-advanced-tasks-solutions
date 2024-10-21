from .base_token_validation_service import BaseTokenValidationService


class UserLogoutService(BaseTokenValidationService[None]):

    async def act(self) -> None:
        access_token = await self.get_validated_token()
        await self.session.delete(access_token)
        await self.session.commit()
