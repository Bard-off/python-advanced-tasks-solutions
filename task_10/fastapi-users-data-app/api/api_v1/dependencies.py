from fastapi import Depends

from core.schemas.token_introspect import TokenIntrospect
from core.schemas.user import UserMinimalDetails, UserPublicDetails
from crud.user_details.get_optional_token_introspect_service import (
    get_optional_token_introspect,
)


def user_is_authenticated(
    token: TokenIntrospect | None = Depends(get_optional_token_introspect),
) -> bool:
    return bool(token)


def get_user_schema(
    is_authenticated: bool = Depends(user_is_authenticated),
) -> type[UserMinimalDetails | UserPublicDetails]:
    if is_authenticated:
        return UserPublicDetails
    return UserMinimalDetails
