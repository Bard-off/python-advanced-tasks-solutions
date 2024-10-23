from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.config import settings
from core.models import User
from core.schemas.user import UserMinimalDetails, UserPrivateDetails, UserPublicDetails
from crud.user_details.get_all_users_service import GetAllUsersService
from crud.user_details.get_user_details_service import GetUserDetailsService
from crud.user_details.get_user_private_details_service import (
    get_current_user_private_details,
)

from .dependencies import get_user_schema

router = APIRouter(
    prefix=settings.api.v1.users,
)


@router.get("/", response_model=list[UserMinimalDetails] | list[UserPublicDetails])
async def get_users_view(
    get_users: Annotated[
        GetAllUsersService,
        Depends(GetAllUsersService),
    ],
    schema: type[UserMinimalDetails | UserPublicDetails] = Depends(get_user_schema),
) -> list[UserMinimalDetails | UserPublicDetails]:
    users = await get_users()
    return [schema.model_validate(user) for user in users]


@router.get("/me", response_model=UserPrivateDetails)
async def get_users_private_details(
    user: User = Depends(get_current_user_private_details),
) -> User:
    return user


@router.get("/{id}")
async def get_user_details(
    get_user: Annotated[
        GetUserDetailsService,
        Depends(GetUserDetailsService),
    ],
    schema: type[UserMinimalDetails | UserPublicDetails] = Depends(get_user_schema),
) -> UserMinimalDetails | UserPublicDetails:
    user = await get_user()
    if user:
        return schema.model_validate(user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User #{get_user.object_id} not found",
    )
