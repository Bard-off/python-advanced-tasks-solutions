import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.models import AccessToken, User
from core.schemas.access_token import AccessTokenRead
from core.schemas.access_token_introspect import AccessTokenIntrospect
from core.schemas.user import UserRead
from crud.auth import (
    AccessTokenIntrospectService,
    TokenExpiredError,
    TokenInvalidError,
    UserAlreadyExistsException,
    UserCreateService,
    UserLoginService,
    UserLogoutService,
)

router = APIRouter(tags=["Auth"])


log = logging.getLogger(__name__)


@router.post("/register", response_model=UserRead)
async def user_register(
    register: Annotated[
        UserCreateService,
        Depends(UserCreateService),
    ],
) -> User:
    try:
        user = await register()
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    log.info("Registered user %s", user)
    return user


@router.post("/login", response_model=AccessTokenRead)
async def user_login(
    login: Annotated[
        UserLoginService,
        Depends(UserLoginService),
    ],
) -> AccessToken:
    access_token = await login()
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    log.info(
        "Logged in as user %s with token #%d",
        access_token.user_id,
        access_token.id,
    )
    return access_token


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def user_logout(
    logout: Annotated[
        UserLogoutService,
        Depends(UserLogoutService),
    ],
) -> None:
    try:
        await logout()
    except (TokenInvalidError, TokenExpiredError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    log.info("Logged out user")


@router.get("/introspect", response_model=AccessTokenIntrospect)
async def access_token_introspect(
    introspect: Annotated[
        AccessTokenIntrospectService,
        Depends(AccessTokenIntrospectService),
    ],
) -> AccessToken:
    try:
        token = await introspect()
    except (TokenInvalidError, TokenExpiredError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    log.info(
        "Introspect token #%d for user %s",
        token.id,
        token.user_id,
    )
    return token
