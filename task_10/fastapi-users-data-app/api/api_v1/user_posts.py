from typing import Annotated

from fastapi import APIRouter, Depends

from core.config import settings
from core.models import Post
from core.schemas.post import PostRead
from crud.user_details.get_users_posts_service import GetUsersPostsService

router = APIRouter(
    prefix=settings.api.v1.users,
)


@router.get("/{user_id}/posts", response_model=list[PostRead])
async def get_posts_for_user_view(
    get_posts_for_user: Annotated[
        GetUsersPostsService,
        Depends(GetUsersPostsService),
    ],
) -> list[Post]:
    return await get_posts_for_user()
